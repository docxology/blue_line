"""Figure registry and deterministic build entry points."""

from __future__ import annotations

import json
import shutil
import subprocess
import hashlib
import os
import platform
from pathlib import Path
from ..serialization import registry_digest
from ..version import __version__

from .cover import cover_svg
from .specs import FIGURE_SPECS
from .svg import freshness_window_svg, registry_map_svg, verdict_paths_svg

_BUILDERS = {
    "blue_registry_map": lambda: registry_map_svg(),
    "blue_verdict_paths": lambda: verdict_paths_svg(),
    "blue_freshness_window": lambda: freshness_window_svg(),
    "blue_line_cover": lambda: cover_svg(),
}

FIGURE_REGISTRY_JSON = "figure_registry.json"


def build_all(output_dir: Path) -> dict[str, str]:
    """Build every spec'd figure into ``output_dir``.

    Returns a mapping of figure id to emitted filename, in spec order.
    Writes each ``.svg`` artifact plus a ``figure_registry.json`` manifest
    in the migrated ``fig:`` accessibility format: every entry carries its
    manuscript label, caption, and alt text beside the file metadata.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    emitted: dict[str, str] = {}
    entries: list[dict[str, object]] = []
    for spec in FIGURE_SPECS:
        builder = _BUILDERS[spec.figure_id]
        svg = builder()
        name = f"{spec.figure_id}.svg"
        (output_dir / name).write_text(svg, encoding="utf-8")
        emitted[spec.figure_id] = name
        entries.append(
            {
                "label": spec.label,
                "figure_id": spec.figure_id,
                "title": spec.title,
                "filename": name,
                "caption": spec.description,
                "alt_text": spec.description,
                "bytes": len(svg.encode("utf-8")),
                "source": "blue_line commitment registry and evaluator rules",
                "generated_by": "blue_line.figures.build_all",
                "format": "deterministic SVG",
            }
        )
    cover = next(e for e in entries if e["figure_id"] == COVER_ID)
    registry: dict[str, object] = {
        "schema_version": "2.0",
        "package_version": __version__,
        "registry_digest": registry_digest(),
        "figures": entries,
        # The title-page pointer repeats the cover's registered contract so
        # the manuscript's `paper.cover.image` has something to be bound to.
        "cover": dict(cover),
    }
    payload = json.dumps(registry, indent=2, sort_keys=True) + chr(10)
    (output_dir / FIGURE_REGISTRY_JSON).write_text(payload, encoding="utf-8")
    return emitted


#: The rasterizer this build shells out to, unless the environment names another.
RSVG_CONVERT = "rsvg-convert"

#: The environment variable that overrides the rasterizer.
RSVG_ENV_VAR = "BLUE_LINE_RSVG_CONVERT"

#: The figure rasterized to PNG beside its SVG by :func:`build_cover_png`.
COVER_ID = "blue_line_cover"


def _rasterizer() -> str:
    """Resolve the pinned rasterizer, or fail with install guidance."""

    from os import environ

    named = environ.get(RSVG_ENV_VAR)
    if named:
        return named
    converter = shutil.which(RSVG_CONVERT)
    if converter is None:
        raise RuntimeError(
            f"{RSVG_CONVERT!r} is not an executable on PATH, so the Blue Line "
            "figures cannot be rasterized. Install librsvg (macOS: 'brew "
            "install librsvg'; Debian or Ubuntu: 'apt-get install "
            "librsvg2-bin'; Fedora: 'dnf install librsvg2-tools') so that "
            f"{RSVG_CONVERT!r} is on PATH, or set {RSVG_ENV_VAR} to the "
            "executable to use. The build writes no PNG rather than "
            "reporting a cover it could not render."
        )
    return converter


def build_cover_png(output_dir: Path) -> Path:
    """Rasterize the cover plate's SVG to a PNG beside it.

    Byte identity requires the same SVG, renderer, fonts and environment.
    A sidecar records the executable, version, platform and content hashes.
    """

    return build_png(output_dir, COVER_ID)


def build_png(output_dir: Path, figure_id: str) -> Path:
    output_dir = Path(output_dir)
    if figure_id not in _BUILDERS:
        raise ValueError(f"unknown figure id: {figure_id}")
    svg_path = output_dir / f"{figure_id}.svg"
    if not svg_path.is_file():
        raise FileNotFoundError(
            f"{svg_path} does not exist; run build_all() before build_cover_png()."
        )
    png_path = output_dir / f"{figure_id}.png"
    converter = _rasterizer()
    try:
        version = subprocess.run(
            [converter, "--version"], check=True, capture_output=True, text=True
        ).stdout.strip()
        subprocess.run(
            [converter, str(svg_path), "--output", str(png_path)], check=True
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            f"the rasterizer named by {RSVG_ENV_VAR} disappeared or is not "
            f"executable; repair it and rerun the cover build"
        ) from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"the rasterizer failed while rendering {figure_id} (exit "
            f"{error.returncode}); repair librsvg and rerun the figure build"
        ) from error
    renderer_path = Path(shutil.which(converter) or converter).resolve(strict=True)
    receipt = {
        "schema_version": "blue_line.raster-provenance/1.0",
        "renderer_path": str(renderer_path),
        "renderer_version": version,
        "renderer_sha256": hashlib.sha256(renderer_path.read_bytes()).hexdigest(),
        "platform": platform.platform(),
        "environment": {
            key: os.environ.get(key)
            for key in ("LANG", "LC_ALL", "FONTCONFIG_FILE", "FONTCONFIG_PATH")
        },
        "svg_sha256": hashlib.sha256(svg_path.read_bytes()).hexdigest(),
        "png_sha256": hashlib.sha256(png_path.read_bytes()).hexdigest(),
        "reproduction_boundary": "same renderer, libraries, fonts and environment required; no portable byte identity claimed",
    }
    (output_dir / f"{figure_id}.provenance.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    manifest_path = output_dir / FIGURE_REGISTRY_JSON
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = next(item for item in manifest["figures"] if item["figure_id"] == figure_id)
    entry.update(
        {
            "filename": png_path.name,
            "bytes": png_path.stat().st_size,
            "format": "PNG with renderer provenance",
            "raster_provenance": f"{figure_id}.provenance.json",
        }
    )
    if figure_id == COVER_ID:
        manifest["cover"] = dict(entry)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return png_path
