"""Deterministic figure building and the figure registry."""

from __future__ import annotations

import json
import os
from pathlib import Path

import blue_line
import pytest
from blue_line.figures import FIGURE_SPECS, build_all, build_cover_png, figure_ids
from blue_line.figures.cover import cover_svg
from blue_line.serialization import registry_digest


def test_build_all_emits_svg_and_manifest(tmp_output: Path):
    emitted = build_all(tmp_output)
    assert set(emitted) == set(figure_ids())
    for name in emitted.values():
        text = (tmp_output / name).read_text(encoding="utf-8")
        assert text.startswith("<svg")
    registry = json.loads(
        (tmp_output / "figure_registry.json").read_text(encoding="utf-8")
    )
    assert registry["schema_version"] == "2.0"
    assert registry["package_version"] == blue_line.__version__
    assert registry["registry_digest"] == registry_digest()
    figures = registry["figures"]
    assert [f["figure_id"] for f in figures] == list(figure_ids())
    for entry in figures:
        assert entry["label"] == "fig:" + entry["figure_id"].replace("_", "-")
        assert entry["filename"] == emitted[entry["figure_id"]]
        assert entry["bytes"] > 0
        assert entry["caption"]
        assert entry["alt_text"] == next(
            spec.description
            for spec in FIGURE_SPECS
            if spec.figure_id == entry["figure_id"]
        )
        assert "alt" not in entry


def test_build_is_deterministic(tmp_output: Path):
    build_all(tmp_output)
    first = {p.name: p.read_bytes() for p in sorted(tmp_output.iterdir())}
    build_all(tmp_output)
    second = {p.name: p.read_bytes() for p in sorted(tmp_output.iterdir())}
    assert first == second


def test_cover_svg_is_stable():
    assert cover_svg() == cover_svg()


def test_build_all_includes_cover_in_manifest(tmp_output: Path):
    emitted = build_all(tmp_output)
    assert emitted["blue_line_cover"] == "blue_line_cover.svg"
    registry = json.loads(
        (tmp_output / "figure_registry.json").read_text(encoding="utf-8")
    )
    assert registry["figures"][-1]["figure_id"] == "blue_line_cover"
    assert registry["cover"]["filename"] == "blue_line_cover.svg"
    assert registry["cover"]["label"] == "fig:blue-line-cover"
    assert registry["cover"] == registry["figures"][-1]


def test_cover_png_build_is_deterministic(tmp_output: Path):
    build_all(tmp_output)
    first = build_cover_png(tmp_output)
    first_bytes = first.read_bytes()
    assert first.name == "blue_line_cover.png"
    assert first_bytes[:8] == b"\x89PNG\r\n\x1a\n"
    build_all(tmp_output)
    second = build_cover_png(tmp_output)
    assert first_bytes == second.read_bytes()


def test_png_build_records_renderer_and_content_provenance(tmp_output):
    import hashlib

    build_all(tmp_output)
    png = build_cover_png(tmp_output)
    receipt = json.loads((tmp_output / "blue_line_cover.provenance.json").read_text())
    assert receipt["png_sha256"] == hashlib.sha256(png.read_bytes()).hexdigest()
    assert (
        receipt["svg_sha256"]
        == hashlib.sha256((tmp_output / "blue_line_cover.svg").read_bytes()).hexdigest()
    )
    assert receipt["renderer_version"]
    assert (
        receipt["renderer_sha256"]
        == hashlib.sha256(Path(receipt["renderer_path"]).read_bytes()).hexdigest()
    )
    assert receipt["platform"]


def test_rasterized_figure_registry_points_at_rendered_file(tmp_output):
    from blue_line.figures.build import build_png

    build_all(tmp_output)
    png = build_png(tmp_output, "blue_registry_map")
    registry = json.loads((tmp_output / "figure_registry.json").read_text())
    entry = next(
        e for e in registry["figures"] if e["figure_id"] == "blue_registry_map"
    )
    assert entry["filename"] == png.name
    assert entry["bytes"] == png.stat().st_size
    assert entry["alt_text"] == next(
        spec.description
        for spec in FIGURE_SPECS
        if spec.figure_id == "blue_registry_map"
    )
    assert "alt" not in entry


@pytest.mark.parametrize(
    "failure",
    [
        "missing_source",
        "bad_id",
        "missing_converter",
        "failed_converter",
        "absent_path",
    ],
)
def test_real_raster_failures_are_visible(tmp_output, failure):
    from blue_line.figures.build import build_png

    build_all(tmp_output)
    old_path = os.environ.get("PATH")
    old_converter = os.environ.get("BLUE_LINE_RSVG_CONVERT")
    try:
        if failure == "missing_converter":
            os.environ["BLUE_LINE_RSVG_CONVERT"] = str(tmp_output / "does-not-exist")
        elif failure == "failed_converter":
            os.environ["BLUE_LINE_RSVG_CONVERT"] = "/usr/bin/false"
        elif failure == "absent_path":
            os.environ.pop("BLUE_LINE_RSVG_CONVERT", None)
            os.environ["PATH"] = str(tmp_output)
        target = tmp_output / "absent" if failure == "missing_source" else tmp_output
        name = "unknown" if failure == "bad_id" else "blue_line_cover"
        error_type = (
            FileNotFoundError
            if failure == "missing_source"
            else ValueError
            if failure == "bad_id"
            else RuntimeError
        )
        with pytest.raises(error_type):
            build_png(target, name)
    finally:
        for key, value in (
            ("PATH", old_path),
            ("BLUE_LINE_RSVG_CONVERT", old_converter),
        ):
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
