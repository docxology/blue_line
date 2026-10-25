# AGENTS.md — `blue_line/src`

## Scope
- Committed source tree of this standalone repo (GitHub `docxology/blue_line`).
  Nothing here is a local-only path: no `.gitignore` rule excludes `src/`, and
  no sibling project is required to run anything in this repo.
- Repo-wide contract: root `AGENTS.md`.

## Layout
- `blue_line/` — runtime package; module inventory in `blue_line/README.md`.
- `blue_line/figures/` — deterministic figure builders; notes in
  `blue_line/figures/AGENTS.md`.

## Gotchas
- Runtime code is pure standard library. Dev dependencies (pytest, pytest-cov,
  ruff) are declared in `pyproject.toml` under `[dependency-groups]`.
- Scripts hold no logic; their command bodies live in `blue_line/cli.py` and
  are tested directly.
