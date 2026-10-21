"""Staged evaluation of declared care signals.

Evaluation is deliberately staged: intake normalization runs first, so
malformed input is set aside with notes instead of crashing. Only then are
commitments matched by tag and scored against the fresh signal set. The
output describes declaration coverage and stewardship gaps; it never turns
declared labels into proof of maintenance, a warranty, or permission.
"""

from __future__ import annotations

from datetime import date, datetime

from .enums import FileStatus, StewardshipStatus
from .intake import intake
from .records import (
    Commitment,
    CommitmentFile,
    CommitmentFinding,
    EvaluationContext,
    SignalSurfaces,
    StewardshipReading,
)
from .registry import BLUE_COMMITMENTS
from .serialization import canonical_input, content_digest, registry_digest
from .version import __version__
from .validation import registry_shape_error, validate_registry

#: Signals are stale when older than this many days at the review date.
DEFAULT_MAX_SIGNAL_AGE_DAYS = 180


def _resolve_review_date(as_of: str | date | None) -> date:
    """Resolve the review date the staleness rules are anchored to."""

    if as_of is None:
        return date.today()
    if isinstance(as_of, str):
        try:
            return date.fromisoformat(as_of)
        except ValueError as exc:
            raise ValueError("as_of must be an ISO date in YYYY-MM-DD form") from exc
    if isinstance(as_of, datetime):
        raise TypeError("as_of must be None, an ISO date string, or a datetime.date")
    if isinstance(as_of, date):
        return as_of
    raise TypeError("as_of must be None, an ISO date string, or a datetime.date")


def _resolve_max_age(max_age_days: int | None) -> int | None:
    """Validate the optional freshness window before it changes scoring."""

    if max_age_days is None:
        return None
    if isinstance(max_age_days, bool) or not isinstance(max_age_days, int):
        raise TypeError("max_signal_age_days must be a non-negative integer or None")
    if max_age_days < 0:
        raise ValueError("max_signal_age_days must be non-negative")
    return max_age_days


def _registry_shape_error(commitments: tuple[Commitment, ...]) -> str | None:
    """Return a blocking note when a custom registry cannot be safely scored."""

    return registry_shape_error(commitments)


def _fresh_and_stale(
    file: CommitmentFile,
    review_date: date,
    max_age_days: int | None,
) -> tuple[frozenset[str], frozenset[str]]:
    """Split declared signals into fresh and stale label sets.

    Undated declarations count as fresh. Dated declarations age against the
    review date; records set aside at intake never appear here.
    """

    fresh: set[str] = set(file.evidence)
    stale: set[str] = set()
    window = DEFAULT_MAX_SIGNAL_AGE_DAYS if max_age_days is None else max_age_days
    for signal in file.dated_evidence:
        if signal.noted_on is None:
            fresh.add(signal.label)
            continue
        try:
            noted = date.fromisoformat(signal.noted_on)
        except (TypeError, ValueError):
            continue
        if noted > review_date:
            continue
        age = (review_date - noted).days
        if age <= window:
            fresh.add(signal.label)
        else:
            stale.add(signal.label)
    return frozenset(fresh), frozenset(stale)


def read_with_surfaces(
    file: CommitmentFile,
    *,
    commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS,
    as_of: str | date | None = None,
    max_signal_age_days: int | None = None,
    allow_unknown_tags: bool = True,
) -> tuple[StewardshipReading, tuple[SignalSurfaces, ...]]:
    """Read one declared commitment file against the registry.

    The verdict describes whether each applicable commitment's required care
    signals were declared fresh at the review date. It is a declaration-
    coverage reading only: a MAINTAINED verdict never asserts that the work
    is healthy, that an obligation is discharged, or that anything is safe.
    """

    max_age_days = _resolve_max_age(max_signal_age_days)
    window = DEFAULT_MAX_SIGNAL_AGE_DAYS if max_age_days is None else max_age_days
    if not isinstance(allow_unknown_tags, bool):
        raise TypeError("allow_unknown_tags must be a boolean")
    shape_error = _registry_shape_error(commitments)
    if shape_error is not None:
        return StewardshipReading(
            status=FileStatus.OUTSIDE_SCOPE,
            findings=(),
            intake_notes=(shape_error,),
            read_as_of="",
            registry_version=__version__,
            registry_digest="",
        ), ()

    staged, status, notes = intake(
        file, allow_unknown_tags=allow_unknown_tags
    )
    review_date = _resolve_review_date(as_of)
    context = EvaluationContext(
        input_digest=content_digest(canonical_input(staged)) if staged is not None else "",
        max_signal_age_days=window,
        allow_unknown_tags=allow_unknown_tags,
        evaluator_version=__version__,
        read_as_of=review_date.isoformat(),
    )
    if staged is None:
        return StewardshipReading(
            status=status,
            findings=(),
            intake_notes=notes,
            read_as_of=review_date.isoformat(),
            registry_version=__version__,
            registry_digest=registry_digest(commitments),
            context=context,
        ), ()
    file = staged
    digest = registry_digest(commitments)
    by_id = {c.id: c for c in commitments}
    ordered_ids = [c.id for c in commitments]

    fresh, stale = _fresh_and_stale(file, review_date, max_age_days)
    review_notes = tuple(sorted({
        f"care signal '{signal.label}' dated {signal.noted_on} is future-dated at review and did not count as fresh"
        for signal in file.dated_evidence
        if signal.noted_on is not None and date.fromisoformat(signal.noted_on) > review_date
    }))
    findings: list[CommitmentFinding] = []
    surfaces: list[SignalSurfaces] = []
    for commitment_id in ordered_ids:
        commitment = by_id[commitment_id]
        if not (commitment.tags & file.tags):
            continue
        present: list[str] = []
        missing: list[str] = []
        stale_missing: list[str] = []
        for label in commitment.required_signals:
            if label in fresh:
                present.append(label)
            else:
                missing.append(label)
                if label in stale:
                    stale_missing.append(label)
        surfaces.append(SignalSurfaces(commitment.id, tuple(present), tuple(missing), tuple(stale_missing)))
        if not missing:
            findings.append(
                CommitmentFinding(
                    commitment_id=commitment.id,
                    status=StewardshipStatus.MAINTAINED,
                    reasons=(
                        "all required care signals declared fresh at the review date",
                    ),
                )
            )
        elif stale_missing:
            findings.append(
                CommitmentFinding(
                    commitment_id=commitment.id,
                    status=StewardshipStatus.STALE,
                    reasons=(
                        tuple(
                            f"required care signal '{label}' was not declared fresh"
                            for label in missing
                        )
                        + ("a declared signal aged past the freshness window",)
                    ),
                )
            )
        else:
            findings.append(
                CommitmentFinding(
                    commitment_id=commitment.id,
                    status=StewardshipStatus.NEEDS_ATTENTION,
                    reasons=tuple(
                        f"required care signal '{label}' was not declared fresh"
                        for label in missing
                    ),
                )
            )

    if not findings:
        verdict = FileStatus.OUTSIDE_SCOPE
        notes = notes + (
            "no registry commitment matched the declared tags; nothing was read",
        )
    elif any(f.status is StewardshipStatus.STALE for f in findings):
        verdict = FileStatus.STALE
    elif any(f.status is StewardshipStatus.NEEDS_ATTENTION for f in findings):
        verdict = FileStatus.NEEDS_ATTENTION
    else:
        verdict = FileStatus.MAINTAINED

    return StewardshipReading(
        status=verdict,
        findings=tuple(findings),
        intake_notes=notes,
        read_as_of=review_date.isoformat(),
        registry_version=__version__,
        registry_digest=digest,
        context=context,
        normalized_input=staged,
        review_notes=review_notes,
    ), tuple(surfaces)


def read_file(
    file: CommitmentFile,
    *,
    commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS,
    as_of: str | date | None = None,
    max_signal_age_days: int | None = None,
    allow_unknown_tags: bool = True,
) -> StewardshipReading:
    """Return the reading projection of the single staged evaluation."""

    reading, _surfaces = read_with_surfaces(
        file,
        commitments=commitments,
        as_of=as_of,
        max_signal_age_days=max_signal_age_days,
        allow_unknown_tags=allow_unknown_tags,
    )
    return reading


def invariants_hold(
    commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS,
) -> tuple[tuple[str, bool, str], ...]:
    """Run the registry invariants and return (name, passed, detail) triples."""

    return validate_registry(commitments, canonical=True)
