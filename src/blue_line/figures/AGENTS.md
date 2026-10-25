# AGENTS.md — `blue_line/src/blue_line/figures`

## Scope
- Committed submodule of the `blue_line` package in this standalone repo; no
  sibling checkout, template, or local-only path is involved.

## Layout
- `specs.py`, `svg.py`, `cover.py`, `build.py` — see `README.md` in this
  directory for the one-line inventory.

## Gotchas
- Figures derive from repo data only: no network access, no sibling-repo reads.
- SVG output is reproducible from the repo; PNG output records rasterizer
  provenance in a sidecar because bytes depend on the rendering environment.
- Builds write to `output/figures/`, which is gitignored generated output.
