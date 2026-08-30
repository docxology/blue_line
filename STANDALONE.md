# STANDALONE.md

`blue_line` runs with zero sibling line projects present.

- Install: `uv sync` (no runtime dependencies; dev group only).
- Tests: `uv run pytest tests/ --cov=src --cov-report=term` — no sibling is
  imported. The one sibling-aware test skips itself when the sibling
  envelope directory is absent, and asserts against a frozen copy of the
  schema otherwise.
- Figures: `uv run python scripts/build_figures.py` — local data only.
- Rendering: PDF/HTML rendering happens through the external template
  checkout, with this project addressed by the qualified name
  `working/blue_line` (sidecar `working/blue_line` → `projects/working/blue_line`).
  Nothing in this repo requires that checkout to exist.
