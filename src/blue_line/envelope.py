"""Witness envelope construction for Blue Line readings.

An envelope is the flat, field-for-field structure the shared witness
register consumes (schema ``line.report-envelope/1.0``). It records the
verdict, the registry identity that produced it, and the non-claims scope.
It never upgrades a declaration-coverage reading into a maintenance
certificate.
"""

from __future__ import annotations

from .enums import FileStatus
from .records import StewardshipReading
from .serialization import reading_digest

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

    return reading.status is not FileStatus.OUTSIDE_SCOPE or bool(reading.findings)


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

    return {
        "schema_version": ENVELOPE_SCHEMA,
        "line_id": BLUE_LINE_ID,
        "native_status": reading.status.value,
        "registry_version": reading.registry_version,
        "registry_digest": reading.registry_digest,
        "report_ref": reading_digest(reading),
        "review_date": reading.read_as_of,
        "scope_and_nonclaims": list(SCOPE_AND_NONCLAIMS),
        "source_snapshot_refs": list(source_snapshot_refs),
        "subject_id": subject_id,
    }
