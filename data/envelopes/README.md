# envelopes

Current prepared `line.report-envelope/1.0` envelopes for the worked declaration
and the shared-subject example. These are transport inputs, not evidence of
witness-register admission or actual maintenance.

From the repository root, run `uv run python scripts/gen_examples.py` to derive
them from `data/declared_files/` and `data/example_contexts.json`, together with
companion replay reports in `data/reports/` and subject-bound bindings in
`data/report_bindings/`. Existing generated outputs are never inputs: deleting
or corrupting them does not change regeneration. Contexts explicitly retain
subject IDs, review dates and declared source references; historical subject
references are not current publication claims.
Do not hand-edit hashes or copy these inputs into sibling repositories as part
of generation.
