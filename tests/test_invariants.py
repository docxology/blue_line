"""Canonical registry sorting behavior."""

from __future__ import annotations

from blue_line.serialization import canonical_registry


def test_canonical_registry_sorts_before_emit():
    payload = canonical_registry()
    assert payload["tag_vocabulary"] == sorted(payload["tag_vocabulary"])
    for commitment in payload["commitments"]:
        assert commitment["tags"] == sorted(commitment["tags"])
