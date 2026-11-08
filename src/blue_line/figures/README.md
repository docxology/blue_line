# figures

Deterministic figure building. Every figure is derived from repo data; no
network access and no sibling-repo reads.

| Module | Contents |
|--------|----------|
| `specs.py` | Figure specifications (id, title, kind) the builder emits |
| `svg.py` | Deterministic SVG emission from derived data |
| `cover.py` | Cover plate (title-page motif), emitted as PNG |
| `build.py` | Figure registry, build entry points, raster provenance sidecar |

Build with `uv run python scripts/build_figures.py`, which writes into
`output/figures/` (gitignored generated output). SVG bytes are reproducible
from the repo; PNG bytes depend on the rasterizer environment, so the build
records raster provenance in a sidecar rather than claiming byte-identical
PNG reproduction.

The current `figure_registry.json` uses metadata schema `2.0`. Each figure
and the repeated cover entry carry authored accessibility text under
`alt_text`, with no serialized `alt` alias or caption fallback. Rasterizing
a figure changes its file metadata while preserving its accessibility text.

Every publication SVG includes the cover's opaque house-paper canvas.
Its dark labels therefore retain their intended contrast when an SVG or PNG
is embedded in a dark reader. Native rasterization controls exercise both
light and dark reader backgrounds without disabling the reader's theme.
