"""Sorting discipline and claim-boundary invariants."""

from __future__ import annotations

from pathlib import Path

from blue_line.serialization import canonical_registry

REPO = Path(__file__).resolve().parents[1]


def test_canonical_registry_sorts_before_emit():
    payload = canonical_registry()
    assert payload["tag_vocabulary"] == sorted(payload["tag_vocabulary"])
    for commitment in payload["commitments"]:
        assert commitment["tags"] == sorted(commitment["tags"])


def test_claim_boundaries_doc_exists():
    doc = REPO / "docs" / "claim_boundaries.md"
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    assert "never" in text.lower()


def test_no_hardcoded_digest_in_sources():
    """No source file may embed a full sha256 hex digest literal."""

    import re

    pattern = re.compile(r"[0-9a-f]{64}")
    offenders = []
    for tree in ("src", "scripts"):
        for path in sorted((REPO / tree).rglob("*.py")):
            if pattern.search(path.read_text(encoding="utf-8")):
                offenders.append(str(path.relative_to(REPO)))
    assert offenders == []
