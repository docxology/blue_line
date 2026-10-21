# blue_line

A stewardship instrument for maintained commitments: systems, obligations,
and relationships to past work.

`blue_line` is the blue colour in the docxology line set. It answers one
question — **What must I keep working?** — by reading a declared file of
commitments against a versioned registry and returning a verdict that
describes declaration coverage of care signals at a review date.

## What it is

- A versioned registry of keepable commitments, each with required
  care signals (handover notes, check runs, response logs, cadence
  statements).
- A fail-closed staged intake that sets aside malformed input with notes
  rather than crashing or inventing values.
- An evaluator that returns MAINTAINED / NEEDS_ATTENTION / STALE /
  OUTSIDE_SCOPE, plus per-commitment signal surfaces.
- Deterministic figure builders, a generated formalism ledger, and
  witness-register envelopes prepared for admission.
- Replay reports binding normalized declarations, effective policy and evaluator
  version, plus a declaration-level worklist derived from the same surfaces.

## What it is never

A warranty, SLA, availability guarantee, or proof of maintenance. A
MAINTAINED verdict is a declaration-coverage statement: it says the steward
declared the required care signals fresh at the review date. It does not
verify the care happened, and it never authorizes an action. See
[docs/claim_boundaries.md](docs/claim_boundaries.md), the register of record.

## Usage

```bash
uv sync
uv run pytest tests/ --cov=src --cov-report=term
uv run ruff check src tests scripts
uv run python scripts/build_figures.py
uv run python scripts/check_registry.py
uv run python scripts/read_file_cli.py '{"description": "my repo", "tags": ["code", "docs"], "evidence": ["handover_note"]}'
uv run python scripts/gen_formalism_ledger.py
uv run python scripts/check_publication.py
```

Pure standard library at runtime; dev dependencies are pytest, pytest-cov,
and ruff only. The repo installs, tests, checks, builds figures, and renders
with zero sibling line projects present; sibling absence is an explicit
NOT_INSTALLED outcome, never an exception.

The CLI deliberately resolves an omitted `--as-of` to the current local date.
Pass `--as-of YYYY-MM-DD` for replay. Every successful output exposes the resolved
date, effective freshness window and registry identity. Invalid JSON syntax or
shape exits with code 2; a well-formed unmatched declaration returns OUTSIDE_SCOPE.
Labels and dated records must be JSON arrays, never objects, strings or null
containers. Optional `declared_owner`, `declared_next_review` (ISO date) and
`source_reference` describe file-level declarations, not verified obligations.

See [the report contract](docs/reports.md) for projection versus replay identity,
schema migration, intake-container policy and envelope eligibility, and
[publication](docs/publication.md) for the reserve-first DOI procedure.

## The Line Set

This work is one of ten in the Line Set family — eight instruments, their
cross-line reader, and the witness register that co-registers their report
envelopes without aggregation:

- [Black Line](https://github.com/docxology/black_line) — the practice registry of realized craft
- [Golden Line](https://github.com/docxology/golden_line) — the aspiration and horizon registry
- [Red Line](https://github.com/docxology/red_line) — the cognitive-security registry of self-assessments
- [White Line](https://github.com/docxology/white_line) — the absence and omission ledger
- [Silver Line](https://github.com/docxology/silver_line) — the memory-and-succession instrument
- [Violet Line](https://github.com/docxology/violet_line) — the consent ledger of affected parties
- [Green Line](https://github.com/docxology/green_line) — the capacity-under-development instrument
- [The Line Set](https://github.com/docxology/line_set) — the cross-line set reader holding instruments apart
- [The Witness Register](https://github.com/docxology/witness_register) — co-registration without aggregation
