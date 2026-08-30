"""Figure registry and deterministic build entry points."""

from __future__ import annotations

import json
from pathlib import Path

from .specs import FIGURE_SPECS
from .svg import freshness_window_svg, registry_map_svg, verdict_paths_svg

_BUILDERS = {
    "blue_registry_map": lambda: registry_map_svg(),
    "blue_verdict_paths": lambda: verdict_paths_svg(),
    "blue_freshness_window": lambda: freshness_window_svg(),
}

FIGURE_REGISTRY_JSON = "figure_registry.json"


def build_all(output_dir: Path) -> dict[str, str]:
    """Build every spec'd figure into ``output_dir``.

    Returns a mapping of figure id to emitted filename, in spec order.
    Writes each ``.svg`` artifact plus a ``figure_registry.json`` manifest
    recording the spec, file, and byte size of every figure.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    emitted: dict[str, str] = {}
    manifest: list[dict[str, object]] = []
    for spec in FIGURE_SPECS:
        builder = _BUILDERS[spec.figure_id]
        svg = builder()
        name = f"{spec.figure_id}.svg"
        (output_dir / name).write_text(svg, encoding="utf-8")
        emitted[spec.figure_id] = name
        manifest.append(
            {
                "figure_id": spec.figure_id,
                "title": spec.title,
                "file": name,
                "bytes": len(svg.encode("utf-8")),
            }
        )
    payload = json.dumps(manifest, indent=2, sort_keys=True) + chr(10)
    (output_dir / FIGURE_REGISTRY_JSON).write_text(payload, encoding="utf-8")
    return emitted
