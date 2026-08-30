"""Canonical serialization: sorted before emit; digests derived, stable."""

from __future__ import annotations

import json

from blue_line.evaluator import read_file
from blue_line.records import CommitmentFile
from blue_line.serialization import (
    canonical_reading,
    canonical_registry,
    reading_digest,
    registry_digest,
)


def test_canonical_registry_is_json_and_sorted():
    payload = canonical_registry()
    text = json.dumps(payload, sort_keys=True)
    assert "commitments" in text
    assert payload["tag_vocabulary"] == sorted(payload["tag_vocabulary"])


def test_registry_digest_stable():
    assert registry_digest() == registry_digest()


def test_registry_digest_changes_with_content():
    from blue_line.records import Commitment
    from blue_line.registry import BLUE_COMMITMENTS

    extra = BLUE_COMMITMENTS + (
        Commitment("zz-extra", "Extra", "wire", frozenset({"code"}), ("s",)),
    )
    assert registry_digest(extra) != registry_digest()


def test_canonical_reading_sorted_and_json():
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code", "docs"})),
        as_of="2026-08-01",
    )
    payload = canonical_reading(reading)
    text = json.dumps(payload, sort_keys=True)
    assert text
    ids = [f["commitment_id"] for f in payload["findings"]]
    assert ids == sorted(ids)


def test_reading_digest_differs_for_different_verdicts():
    a = read_file(
        CommitmentFile(description="x", tags=frozenset({"code", "docs"})),
        as_of="2026-08-01",
    )
    b = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        as_of="2026-08-01",
    )
    assert reading_digest(a) != reading_digest(b)
