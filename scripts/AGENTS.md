# scripts — agent notes

Thin orchestrators only: path bootstrap, argument handling, and logging;
computation lives in `src/blue_line/`. Each script inserts `src/` on
sys.path and imports the package. Command bodies moved out of scripts are
importable and tested directly (`blue_line.cli.read_file_main`,
`blue_line.ledger.build_formalism_ledger`, `blue_line.ledger.write_formalism_ledger`
in `tests/test_cli.py` and `tests/test_ledger.py`); every script also has
subprocess coverage in `tests/test_scripts_cli.py`.

## Inventory

| Script | Contract | Delegates to |
|--------|----------|--------------|
| `build_figures.py` | Builds every declared figure plus the cover PNG into `output/figures/`; prints one line per artifact | `blue_line.figures.build_all`, `blue_line.figures.build_cover_png` |
| `check_registry.py` | Runs the registry invariants; prints one PASS/FAIL line per invariant; exit 1 on any failure | `blue_line.invariants_hold` |
| `gen_formalism_ledger.py` | Regenerates `data/formalism_claim_ledger.json` from the live package; the file is a derived projection, never edited by hand | `blue_line.ledger.write_formalism_ledger` |
| `read_file_cli.py` | Reads one declared commitment file as a JSON object on argv (optional `--as-of YYYY-MM-DD`, default `2026-08-01`); prints the reading verdict, intake notes, per-commitment findings, and signal surfaces as JSON; exit 2 on usage or JSON errors | `blue_line.cli.read_file_main` |

Do not add business, data, or plot logic to scripts; put it in
`src/blue_line/` and delegate.
