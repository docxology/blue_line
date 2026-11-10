"""Witness envelope construction for Blue Line readings.

An envelope is the flat, field-for-field structure the shared witness
register consumes (schema ``line.report-envelope/1.0``). It records the
verdict, the registry identity that produced it, and the non-claims scope.
It never upgrades a declaration-coverage reading into a maintenance
certificate.
"""

from __future__ import annotations

from datetime import date
import re

from .enums import FileStatus
from .records import EvaluationContext, StewardshipReading
from .serialization import canonical_input, content_digest, reading_digest

ENVELOPE_SCHEMA = "line.report-envelope/1.0"
BLUE_LINE_ID = "blue_line"

SCOPE_AND_NONCLAIMS = (
    "describes declaration coverage of self-declared care signals at a stated review date",
    "not a maintenance, warranty, SLA, availability, or support claim",
    "not permission: MAINTAINED never authorizes an action, a route, or a release",
    "does not verify that a declared care signal exists or supports what it names",
    "does not rank, merge, or evaluate the other line instruments",
)


def envelope_matches_reading(reading: StewardshipReading) -> bool:
    """Return True when the reading can be turned into an envelope."""

    if reading.status is FileStatus.OUTSIDE_SCOPE or not reading.findings:
        return False
    if not isinstance(reading.registry_version, str) or not reading.registry_version.strip():
        return False
    if not isinstance(reading.registry_digest, str) or re.fullmatch(r"[0-9a-f]{64}", reading.registry_digest) is None:
        return False
    try:
        parsed = date.fromisoformat(reading.read_as_of)
    except (TypeError, ValueError):
        return False
    context = reading.context
    return (
        parsed.isoformat() == reading.read_as_of
        and isinstance(context, EvaluationContext)
        and context.schema_version == "blue_line.evaluation-context/1.0"
        and isinstance(context.max_signal_age_days, int)
        and not isinstance(context.max_signal_age_days, bool)
        and context.max_signal_age_days >= 0
        and isinstance(context.allow_unknown_tags, bool)
        and context.read_as_of == reading.read_as_of
        and context.evaluator_version == reading.registry_version
        and reading.normalized_input is not None
        and context.input_digest == content_digest(canonical_input(reading.normalized_input))
    )


class EnvelopeEligibilityError(ValueError):
    def __init__(self, field: str) -> None:
        self.field = field
        super().__init__(f"{field}: envelope requires an applicable reading and nonblank identifiers")


def _is_scalar_text(value: object) -> bool:
    return isinstance(value, str) and not any(
        0xD800 <= ord(character) <= 0xDFFF for character in value
    )


def build_envelope(
    reading: StewardshipReading,
    *,
    subject_id: str,
    source_snapshot_refs: tuple[str, ...] = (),
) -> dict[str, object]:
    """Return the witness-register envelope fields for one reading.

    ``report_ref`` is the SHA-256 digest of the canonical reading, computed
    here rather than hardcoded anywhere.
    """

    if not envelope_matches_reading(reading):
        raise EnvelopeEligibilityError("reading")
    if (
        not _is_scalar_text(subject_id)
        or not subject_id.strip()
        or subject_id != subject_id.strip()
    ):
        raise EnvelopeEligibilityError("subject_id")
    if not isinstance(source_snapshot_refs, tuple) or any(
        not _is_scalar_text(ref) or not ref.strip() or ref != ref.strip()
        for ref in source_snapshot_refs
    ):
        raise EnvelopeEligibilityError("source_snapshot_refs")
    return {
        "schema_version": ENVELOPE_SCHEMA,
        "line_id": BLUE_LINE_ID,
        "native_status": reading.status.value,
        "registry_version": reading.registry_version,
        "registry_digest": reading.registry_digest,
        "report_ref": reading_digest(reading),
        "review_date": reading.read_as_of,
        "scope_and_nonclaims": list(SCOPE_AND_NONCLAIMS),
        "source_snapshot_refs": sorted(set(source_snapshot_refs)),
        "subject_id": subject_id,
    }


def envelope_digest(envelope: dict[str, object]) -> str:
    return content_digest(envelope)
