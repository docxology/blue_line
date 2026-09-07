"""The ledger builder derives its payload from the live package."""

from __future__ import annotations

import hashlib
import json

from blue_line.ledger import LEDGER_SCHEMA, build_formalism_ledger, write_formalism_ledger


def test_build_formalism_ledger_digest_covers_payload():
    payload = build_formalism_ledger()
    body = {k: v for k, v in payload.items() if k != "ledger_digest"}
    expected = hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()
    assert payload["ledger_digest"] == expected


def test_build_formalism_ledger_schema_and_vocabulary():
    payload = build_formalism_ledger()
    assert payload["schema"] == LEDGER_SCHEMA
    assert payload["registry_digest"]
    assert payload["commitments"]
    assert payload["figures"]


def test_write_formalism_ledger_writes_data_file(tmp_path):
    out = write_formalism_ledger(tmp_path)
    assert out == tmp_path / "data" / "formalism_claim_ledger.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data == build_formalism_ledger()
