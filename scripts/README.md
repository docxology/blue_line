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
