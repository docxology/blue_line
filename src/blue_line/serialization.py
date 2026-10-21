"""Canonical serialization and digests for the Blue Line registry and readings.

Unordered vocabulary and tags are sorted. Registry commitment order and
required-signal tuple order are semantic and preserved, as in the published
registry digest definition. The legacy reading digest identifies only a
coverage projection; replay identity also binds input, policy and version.
"""

from __future__ import annotations

import hashlib
import json

from dataclasses import asdict

from .records import Commitment, CommitmentFile, EvaluationContext, StewardshipReading
from .registry import BLUE_COMMITMENTS, COMMITMENT_TAG_VOCABULARY


def canonical_registry(
    commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS,
) -> dict[str, object]:
    """Return ordered registry content with sorted unordered fields."""

    return {
        "tag_vocabulary": sorted(COMMITMENT_TAG_VOCABULARY),
        "commitments": [c.canonical() for c in commitments],
    }


def registry_digest(commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS) -> str:
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
    """Hash the legacy projection, excluding input, policy and registry version."""

    payload = json.dumps(canonical_reading(reading), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def content_digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()


def canonical_input(file: CommitmentFile) -> dict[str, object]:
    return {
        "description": file.description,
        "tags": sorted(file.tags),
        "evidence": sorted(file.evidence),
        "dated_evidence": [asdict(s) for s in sorted(file.dated_evidence, key=lambda s: (s.label, s.noted_on or ""))],
        "declared_owner": file.declared_owner,
        "declared_next_review": file.declared_next_review,
        "source_reference": file.source_reference,
    }


def context_digest(context: EvaluationContext) -> str:
    return content_digest(asdict(context))


def replay_digest(reading: StewardshipReading) -> str:
    """Bind context and registry version separately from the legacy projection."""
    return content_digest({
        "schema_version": "blue_line.replay/1.0",
        "projection": canonical_reading(reading),
        "registry_version": reading.registry_version,
        "context": asdict(reading.context) if reading.context is not None else None,
        "review_notes": list(reading.review_notes),
    })
