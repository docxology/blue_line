"""Deterministic figure building and the figure registry."""

from __future__ import annotations

import json
from pathlib import Path

from blue_line.figures import FIGURE_SPECS, build_all, figure_ids


def test_at_least_three_figures():
    assert len(FIGURE_SPECS) >= 3


def test_figure_ids_match_spec_order():
    assert figure_ids() == tuple(s.figure_id for s in FIGURE_SPECS)


def test_build_all_emits_svg_and_manifest(tmp_output: Path):
    emitted = build_all(tmp_output)
    assert set(emitted) == set(figure_ids())
    for name in emitted.values():
        text = (tmp_output / name).read_text(encoding="utf-8")
        assert text.startswith("<svg")
    manifest_path = tmp_output / "figure_registry.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert [m["figure_id"] for m in manifest] == list(figure_ids())
    for entry in manifest:
        assert entry["bytes"] > 0


def test_build_is_deterministic(tmp_output: Path):
    build_all(tmp_output)
    first = {
        p.name: p.read_text(encoding="utf-8") for p in sorted(tmp_output.glob("*.svg"))
    }
    build_all(tmp_output)
    second = {
        p.name: p.read_text(encoding="utf-8") for p in sorted(tmp_output.glob("*.svg"))
    }
    assert first == second
