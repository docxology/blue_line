# src

Source tree for the `blue_line` package.

- `blue_line/` — runtime package: versioned registry, fail-closed staged
  intake, evaluator, canonical serialization and digests, replay reports,
  witness-register envelopes, the formalism ledger, and the command bodies
  behind `scripts/` (see `blue_line/README.md`).
- `blue_line/figures/` — deterministic figure specifications and SVG/PNG
  builders (see `blue_line/figures/README.md`).

Pure standard library at runtime; the development group (pytest, pytest-cov,
ruff) is declared in `pyproject.toml`. Install, test and lint commands are in
the root `README.md` and `docs/development.md`.
