# Development

## Setup

The figure, registry and ledger checks rasterize through `rsvg-convert`, which
is not a Python dependency: install librsvg (`apt-get install librsvg2-bin` on
Debian/Ubuntu, `brew install librsvg` on macOS) so that it is on `PATH`.

```bash
uv sync
uv run pytest tests/ --cov=src --cov-report=term
uv run ruff check src tests scripts
```

## Layout rules

- Business logic only in `src/blue_line/`. Scripts under `scripts/` are thin
  orchestrators that import from the package.
- Runtime code is pure standard library: `from __future__ import annotations`,
  frozen dataclasses, module docstrings bounding claims.
- No mocking framework. Exercise absent/failing input with plain records and
  real temp dirs; the no-mocks test enforces this lexically.
- Sort before emit. Digests and readings must never depend on dict or set
  iteration order (tested in test_serialization and test_invariants).

## Regenerating derived data

```bash
uv run python scripts/gen_formalism_ledger.py   # data/formalism_claim_ledger.json
uv run python scripts/build_figures.py          # output/figures/
```

`uv run python scripts/gen_examples.py` regenerates envelopes and companion
replay reports under `data/`; tests assert live reproducibility and replay.
The formalism generator also emits manuscript variables under `output/data/`.
After a successful render, `uv run python scripts/build_manuscript_bundle.py`
packages the full web tree (including local font loader and favicon), figures
and PDF. Inspect the extracted bundle before distributing it.

The 0.3.1 change updates documentation and publication metadata only. Refresh
current examples, manuscript variables, figures, renderer provenance, and rendered
manuscript outputs from the final source before preparing new release evidence.
Do not overwrite historical `docs/releases/` packets or relabel their receipts.
Blue's inputs and outputs must not contain private sibling source or provenance.

## Release process

See [publication.md](publication.md) for the complete release procedure.
The suite, coverage floor, ruff, `uvx --from basedpyright basedpyright src/blue_line --level error`,
figure/registry/ledger/example regeneration and publication consistency check
are release gates. Runtime remains pure standard library; the type checker
runs as an isolated tool, not a project dependency.

Generic programming-skill library defaults are adapted to this repository's
standard-library runtime and fixed development dependency contract. Existing
lint settings and Python requirements are preserved.

The type gate checks error-severity diagnostics. The checker's recommended
warning profile also reports dynamic JSON types and deliberate runtime guards
of annotated records; no claim of a warning-free recommended-profile run is made.
