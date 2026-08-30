"""The generated formalism ledger reflects the live package, not prose."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "data" / "formalism_claim_ledger.json"


def _load() -> dict:
    assert LEDGER.exists(), "run scripts/gen_formalism_ledger.py first"
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def test_ledger_schema_and_digest():
    data = _load()
    body = {k: v for k, v in data.items() if k != "ledger_digest"}
    expected = hashlib.sha256(
        json.dumps(body, sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert data["ledger_digest"] == expected


def test_ledger_registry_digest_matches_package():
    from blue_line.serialization import registry_digest

    assert _load()["registry_digest"] == registry_digest()


def test_ledger_commitments_match_registry():
    from blue_line.registry import BLUE_COMMITMENTS

    ledger_ids = [c["id"] for c in _load()["commitments"]]
    assert ledger_ids == [c.id for c in BLUE_COMMITMENTS]


def test_ledger_figures_match_specs():
    from blue_line.figures import figure_ids

    assert [f["figure_id"] for f in _load()["figures"]] == list(figure_ids())


def test_ledger_verdict_vocabularies():
    from blue_line.enums import CommitmentKind, FileStatus, StewardshipStatus

    data = _load()
    assert data["kinds"] == sorted(k.value for k in CommitmentKind)
    assert data["file_verdicts"] == sorted(v.value for v in FileStatus)
    assert data["commitment_verdicts"] == sorted(v.value for v in StewardshipStatus)
