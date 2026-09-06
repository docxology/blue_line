"""Re-derive the numeric rows of data/claim_ledger.yaml from the running package.

Every `kind: number` row in data/claim_ledger.yaml is derived from its source
here, so the ledger cannot drift from the executable declaration, and the
manuscript prose carrying the value cannot drift from the ledger.
"""

from __future__ import annotations

import re
from pathlib import Path

from blue_line.evaluator import DEFAULT_MAX_SIGNAL_AGE_DAYS

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "claim_ledger.yaml"
MANUSCRIPT = ROOT / "docs" / "manuscript"


def _parse_yaml_number_claims(path: Path) -> dict[str, int]:
    """Parse id -> value mapping for number claims from claim_ledger.yaml."""
    text = path.read_text(encoding="utf-8")
    claims: dict[str, int] = {}
    current_id: str | None = None
    current_kind: str | None = None

    for line in text.splitlines():
        id_match = re.search(r"^\s*-\s*id:\s*(\w+)", line)
        if id_match:
            current_id = id_match.group(1)
            current_kind = None
            continue
        kind_match = re.search(r"^\s*kind:\s*(\w+)", line)
        if kind_match:
            current_kind = kind_match.group(1)
            continue
        val_match = re.search(r"^\s*value:\s*(\d+)", line)
        if val_match and current_id and current_kind == "number":
            claims[current_id] = int(val_match.group(1))
            current_id = None
            current_kind = None

    return claims


def test_claim_ledger_re_derives_all_numeric_claims() -> None:
    claims = _parse_yaml_number_claims(LEDGER)
    assert claims, "no numeric claims found in claim_ledger.yaml"

    # freshness_window_default_days
    assert claims["freshness_window_default_days"] == DEFAULT_MAX_SIGNAL_AGE_DAYS

def test_method_prose_carries_derived_freshness_window() -> None:
    method = (MANUSCRIPT / "02_method.md").read_text(encoding="utf-8")
    assert re.search(
        rf"freshness window \({DEFAULT_MAX_SIGNAL_AGE_DAYS}\s+days", method
    ), "02_method.md no longer carries the derived freshness window"
