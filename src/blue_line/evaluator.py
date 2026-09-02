"""Staged evaluation of declared care signals.

Evaluation is deliberately staged: intake normalization runs first, so
malformed input is set aside with notes instead of crashing. Only then are
commitments matched by tag and scored against the fresh signal set. The
output describes declaration coverage and stewardship gaps; it never turns
declared labels into proof of maintenance, a warranty, or permission.
"""

from __future__ import annotations

from datetime import date, datetime

from .enums import CommitmentKind, FileStatus, StewardshipStatus
from .intake import intake
from .records import (
    Commitment,
    CommitmentFile,
    CommitmentFinding,
    SignalSurfaces,
    StewardshipReading,
)
from .registry import BLUE_COMMITMENTS, COMMITMENT_TAG_VOCABULARY
from .serialization import registry_digest
from .version import __version__

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

    seen_ids: set[str] = set()
    for index, commitment in enumerate(commitments):
        if not isinstance(commitment, Commitment):
            return f"commitment registry entry {index} is not a Commitment record"
        if any(
            not isinstance(value, str) or not value.strip()
            for value in (commitment.id, commitment.title, commitment.wire)
        ):
            return f"commitment registry entry {index} has blank or non-text fields"
        if commitment.id in seen_ids:
            return f"commitment registry contains duplicate id '{commitment.id}'"
        seen_ids.add(commitment.id)
        if (
            not isinstance(commitment.tags, frozenset)
            or not commitment.tags
            or any(not isinstance(tag, str) or not tag.strip() for tag in commitment.tags)
        ):
            return f"commitment '{commitment.id}' has malformed tags"
        if (
            not isinstance(commitment.required_signals, tuple)
            or not commitment.required_signals
            or any(
                not isinstance(label, str) or not label.strip()
                for label in commitment.required_signals
            )
        ):
            return f"commitment '{commitment.id}' has malformed required signals"
        if not isinstance(commitment.kind, CommitmentKind):
            return f"commitment '{commitment.id}' has an invalid kind"
    return None


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


def read_file(
    file: CommitmentFile,
    *,
    commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS,
    as_of: str | date | None = None,
    max_signal_age_days: int | None = None,
    allow_unknown_tags: bool = True,
) -> StewardshipReading:
    """Read one declared commitment file against the registry.

    The verdict describes whether each applicable commitment's required care
    signals were declared fresh at the review date. It is a declaration-
    coverage reading only: a MAINTAINED verdict never asserts that the work
    is healthy, that an obligation is discharged, or that anything is safe.
    """

    max_age_days = _resolve_max_age(max_signal_age_days)
    shape_error = _registry_shape_error(commitments)
    if shape_error is not None:
        return StewardshipReading(
            status=FileStatus.OUTSIDE_SCOPE,
            findings=(),
            intake_notes=(shape_error,),
            read_as_of="",
            registry_version=__version__,
            registry_digest="",
        )

    staged, status, notes = intake(
        file, allow_unknown_tags=allow_unknown_tags
    )
    review_date = _resolve_review_date(as_of)
    if staged is None:
        return StewardshipReading(
            status=status,
            findings=(),
            intake_notes=notes,
            read_as_of=review_date.isoformat(),
            registry_version=__version__,
            registry_digest=registry_digest(commitments),
        )
    file = staged
    digest = registry_digest(commitments)
    by_id = {c.id: c for c in commitments}
    ordered_ids = [c.id for c in commitments]

    fresh, stale = _fresh_and_stale(file, review_date, max_age_days)
    findings: list[CommitmentFinding] = []
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
    )


def read_with_surfaces(
    file: CommitmentFile,
    *,
    commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS,
    as_of: str | date | None = None,
    max_signal_age_days: int | None = None,
    allow_unknown_tags: bool = True,
) -> tuple[StewardshipReading, tuple[SignalSurfaces, ...]]:
    """Read one file and also return per-commitment signal surfaces."""

    reading = read_file(
        file,
        commitments=commitments,
        as_of=as_of,
        max_signal_age_days=max_signal_age_days,
        allow_unknown_tags=allow_unknown_tags,
    )
    staged, _status, _notes = intake(file, allow_unknown_tags=allow_unknown_tags)
    if staged is None or reading.registry_digest == "":
        return reading, ()
    review_date = _resolve_review_date(as_of)
    max_age_days = _resolve_max_age(max_signal_age_days)
    fresh, stale = _fresh_and_stale(staged, review_date, max_age_days)
    by_id = {c.id: c for c in commitments}
    surfaces: list[SignalSurfaces] = []
    for finding in reading.findings:
        commitment = by_id[finding.commitment_id]
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
        surfaces.append(
            SignalSurfaces(
                commitment_id=commitment.id,
                present=tuple(present),
                missing=tuple(missing),
                stale=tuple(stale_missing),
            )
        )
    return reading, tuple(surfaces)


def invariants_hold(
    commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS,
) -> tuple[tuple[str, bool, str], ...]:
    """Run the registry invariants and return (name, passed, detail) triples."""

    results: list[tuple[str, bool, str]] = []
    ids = [c.id for c in commitments]
    results.append(
        (
            "distinct_commitment_ids",
            len(ids) == len(set(ids)),
            ""
            if len(ids) == len(set(ids))
            else f"duplicates: {sorted(name for name in set(ids) if ids.count(name) > 1)}",
        )
    )
    results.append(
        (
            "min_registry_size",
            len(commitments) >= 6,
            f"{len(commitments)} entries",
        )
    )
    bad_tags = sorted(
        {
            tag
            for c in commitments
            for tag in c.tags
            if tag not in COMMITMENT_TAG_VOCABULARY
        }
    )
    results.append(
        ("tags_in_vocabulary", not bad_tags, f"outside vocabulary: {bad_tags}")
    )
    kinds_used = {c.kind for c in commitments}
    results.append(
        (
            "kind_coverage",
            len(kinds_used) >= 3,
            f"only {sorted(k.value for k in kinds_used)} used",
        )
    )
    blank = [c.id for c in commitments if not c.wire.strip()]
    results.append(("wires_non_blank", not blank, f"blank wires: {blank}"))
    return tuple(results)
