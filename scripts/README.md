# scripts

Thin orchestrator scripts for the Blue Line. Testable logic lives in
`src/blue_line/`; each script only sets up `sys.path` and delegates to one
package entrypoint.

## Inventory

| Script | Purpose | Delegates to | Command |
|--------|---------|--------------|---------|
| `build_figures.py` | Build all declared figures plus the cover plate into `output/figures/` | `blue_line.figures.build_all`, `blue_line.figures.build_cover_png` | `uv run python scripts/build_figures.py` |
| `check_registry.py` | Run the registry invariants and print the PASS/FAIL battery | `blue_line.invariants_hold` | `uv run python scripts/check_registry.py` |
| `gen_formalism_ledger.py` | Regenerate `data/formalism_claim_ledger.json` from the live package | `blue_line.ledger.write_formalism_ledger` | `uv run python scripts/gen_formalism_ledger.py` |
| `read_file_cli.py` | Read one declared commitment file (JSON object on argv, optional `--as-of YYYY-MM-DD`) and print the verdict, intake notes, findings, and signal surfaces as JSON | `blue_line.cli.read_file_main` | `uv run python scripts/read_file_cli.py '{"description": "..."}'` |
| `gen_examples.py` | Regenerate prepared envelopes, companion reports and bindings under `data/` from `data/declared_files/` | `blue_line.examples.write_examples` | `uv run python scripts/gen_examples.py` |
| `check_publication.py` | Check package/pyproject/CITATION/Zenodo version and retained-DOI consistency without external publication | `blue_line.publication.check_publication_main` | `uv run python scripts/check_publication.py` |
| `render_manuscript.py` | Hydrate manuscript variables and invoke PDF/HTML rendering in an explicitly supplied isolated template export | template rendering APIs (`infrastructure.rendering.*` from the export) | `uv run python scripts/render_manuscript.py --template-root <export>` |
| `build_manuscript_bundle.py` | Package the rendered web tree, figures and PDF after a successful render | `blue_line.publication.build_manuscript_bundle` | `uv run python scripts/build_manuscript_bundle.py` |
