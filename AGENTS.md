# AGENTS.md — blue_line working contract

## Identity

`blue_line` is a standalone private repo, the blue colour in the docxology
line set. Question: **What must I keep working?** Job: stewardship of
maintained commitments. It must never become a warranty, SLA, availability
guarantee, or proof of maintenance. Opus stage: None (stageless by design;
see line_set `docs/extensibility.md`).

## Invariants

1. Standalone: everything runs with zero siblings. Sibling absence is an
   outcome (`NOT_INSTALLED` / skipped test), never an exception or a
   fabricated value.
2. Pure standard library at runtime; frozen dataclasses; module docstrings
   bound what the code does and does not establish. Dev deps: pytest,
   pytest-cov, ruff only.
3. No mocking framework anywhere. Absent/failing inputs are exercised with
   plain callables, real records, and fail-closed paths.
4. Fail closed: empty scan set is an OUTSIDE_SCOPE outcome; intake sets
   aside unknown/malformed input with notes.
5. Nothing sorted by accident: sort before emit; no dict/set iteration
   order reaches a reading or digest.
6. Sibling line projects are never modified. line_set and witness_register
   integration is prepared under `data/`, not written into those repos.
7. Claims are underclaimed, first person, narrow; `docs/claim_boundaries.md`
   is the register of record. No number or digest is hardcoded — all are
   derived.

## Verify commands

```bash
uv sync
uv run pytest tests/ --cov=src --cov-report=term   # all green, cov >= 90
uv run ruff check src tests scripts
uv run python scripts/build_figures.py
uv run python scripts/check_registry.py
uv run pytest tests/test_formalism_claim_ledger.py
```

## Layout

- `src/blue_line/` — registry, intake, evaluator, serialization, envelope,
  figures (runtime pure-stdlib package)
- `tests/` — 87 tests incl. no-mocks gate, negative controls, standalone
  envelope-schema checks
- `scripts/` — thin CLIs (build_figures, check_registry, read_file_cli,
  gen_formalism_ledger)
- `data/` — claim ledger, generated formalism ledger, prepared witness
  envelopes, line_set binding declaration
- `docs/` — claim_boundaries, development, extensibility (line-specific),
  releases
- `manuscript/` — the line's manuscript
