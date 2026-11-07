# Extending the blue line

The blue line follows the line set's extension contract
(`line_set/docs/extensibility.md`) from the outside: the set reader takes
the declaration as an argument, so adding blue required no change to the
reader.

## What was prepared here

- `data/binding_declaration.json` — the exact `LineEntry` kwargs a
  maintainer appends to `line_set/src/line_set/registry.py`: id `blue_line`,
  color `blue`, question "What must I keep working?", `opus_stage=None`
  (stageless by design — the four classical stages are allocated), and
  `working_position=None` (assigned at admission, must extend 1..N
  contiguously).
- `data/envelopes/blue_line_worked.json` and `blue_line_same_subject.json`
  — prepared witness-register envelopes in the
  `line.report-envelope/1.0` schema, reproducible from this repo's code by
  test.
- `data/reports/` and `data/report_bindings/` carry replay context and the
  subject-bound envelope-to-report binding without changing the shared schema.

## Adding a commitment to this registry

Append a frozen `Commitment` to `BLUE_COMMITMENTS` in
`src/blue_line/registry.py` with an id unique across the registry, tags from
`COMMITMENT_TAG_VOCABULARY`, and a non-empty ordered tuple of required
signals. The invariants battery (`scripts/check_registry.py`) fails closed
on duplicates, unknown tags, blank fields, and kind imbalance. Regenerate
the formalism ledger afterwards; the registry digest changes by design.

The shared validator separates universal shape from canonical size/kind policy.
Custom library registries may be small, but still use the built-in vocabulary
and unique canonical required labels. Registry order remains part of identity.
