"""Deterministic figure building and the figure registry."""

from __future__ import annotations

import json
from pathlib import Path

from blue_line.figures import FIGURE_SPECS, build_all, build_cover_png, figure_ids
from blue_line.figures.cover import cover_svg


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



def test_cover_spec_is_declared():
    assert "blue_line_cover" in figure_ids()
    assert any(spec.figure_id == "blue_line_cover" for spec in FIGURE_SPECS)


def test_cover_svg_carries_exactly_its_labels():
    svg = cover_svg()
    assert "BLUE LINE" in svg
    assert "MAINTAINED COMMITMENTS, KEPT IN TRUST" in svg
    assert "0.1.0" not in svg
    assert "2025" not in svg
    assert "2026" not in svg


def test_cover_svg_is_stable():
    assert cover_svg() == cover_svg()


def test_build_all_includes_cover_in_manifest(tmp_output: Path):
    emitted = build_all(tmp_output)
    assert emitted["blue_line_cover"] == "blue_line_cover.svg"
    manifest = json.loads((tmp_output / "figure_registry.json").read_text(encoding="utf-8"))
    assert manifest[-1]["figure_id"] == "blue_line_cover"


def test_cover_png_build_is_deterministic(tmp_output: Path):
    build_all(tmp_output)
    first = build_cover_png(tmp_output)
    first_bytes = first.read_bytes()
    assert first.name == "blue_line_cover.png"
    assert first_bytes[:8] == b"\x89PNG\r\n\x1a\n"
    build_all(tmp_output)
    second = build_cover_png(tmp_output)
    assert first_bytes == second.read_bytes()
