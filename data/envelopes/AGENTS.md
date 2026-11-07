# AGENTS.md — `blue_line/data/envelopes`

## Scope
- Current prepared `line.report-envelope/1.0` inputs for external witness-register
  and Line Set consumers. Preparing an envelope is not admission or publication.

## Layout
- `blue_line_worked.json` and `blue_line_same_subject.json` correspond to
  declarations in `../declared_files/` and companion reports and bindings in
  `../reports/` and `../report_bindings/`.

## Gotchas
- Regenerate from the repository root with `uv run python scripts/gen_examples.py`;
  do not hand-edit digests or write into sibling repositories.
- The generator retains each existing subject ID, review date and source snapshot
  references. Historical source identities stay historical even when current
  evaluation reports are regenerated.
- Envelopes describe declared care coverage, never verified maintenance,
  availability, authenticity, or permission.
