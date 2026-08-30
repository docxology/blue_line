"""Canonical serialization and digests for the Blue Line registry and readings.

Every emitted structure sorts before it serializes, so no dict or set
iteration order can reach a digest or a reading. A digest pins the exact
commitment content that produced a verdict.
"""

from __future__ import annotations

import hashlib
import json

from .records import StewardshipReading
from .registry import BLUE_COMMITMENTS, COMMITMENT_TAG_VOCABULARY


def canonical_registry(
    commitments: tuple = BLUE_COMMITMENTS,
) -> dict[str, object]:
    """Return the registry as a sorted, JSON-able canonical structure."""

    return {
        "tag_vocabulary": sorted(COMMITMENT_TAG_VOCABULARY),
        "commitments": [c.canonical() for c in commitments],
    }


def registry_digest(commitments: tuple = BLUE_COMMITMENTS) -> str:
    """Return the SHA-256 digest of the canonical registry content."""

    payload = json.dumps(canonical_registry(commitments), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def canonical_reading(reading: StewardshipReading) -> dict[str, object]:
    """Return a reading as a sorted, JSON-able canonical structure."""

    return {
        "status": reading.status.value,
        "findings": [
            {
                "commitment_id": f.commitment_id,
                "status": f.status.value,
                "reasons": list(f.reasons),
            }
            for f in sorted(reading.findings, key=lambda f: f.commitment_id)
        ],
        "intake_notes": list(reading.intake_notes),
        "read_as_of": reading.read_as_of,
        "registry_digest": reading.registry_digest,
    }


def reading_digest(reading: StewardshipReading) -> str:
    """Return the SHA-256 digest of the canonical reading."""

    payload = json.dumps(canonical_reading(reading), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
