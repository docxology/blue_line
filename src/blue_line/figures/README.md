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
