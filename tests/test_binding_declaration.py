"""The line_set binding declaration: parseable, correct identity fields."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BINDING = REPO / "data" / "binding_declaration.json"

REQUIRED_FIELDS = {
    "id",
    "color",
    "question",
    "job",
    "must_not_become",
    "opus_stage",
    "working_position",
    "package_name",
    "registry_noun",
    "verdict_noun",
}


def test_binding_parses():
    data = json.loads(BINDING.read_text(encoding="utf-8"))
    assert set(data) == REQUIRED_FIELDS


def test_binding_matches_brief():
    data = json.loads(BINDING.read_text(encoding="utf-8"))
    assert data["id"] == "blue_line"
    assert data["color"] == "blue"
    assert data["question"] == "What must I keep working?"
    assert data["must_not_become"] == (
        "A warranty, SLA, availability guarantee, or proof of maintenance"
    )
    assert data["opus_stage"] is None
    assert data["working_position"] is None
    assert data["package_name"] == "blue_line"
