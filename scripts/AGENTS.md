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
| `build_figures.py` | Builds declared SVGs and PNGs with raster provenance into `output/figures/`; binds PNG filenames in the figure registry | `blue_line.figures.build_all`, `blue_line.figures.build.build_png` |
| `check_registry.py` | Runs the registry invariants; prints one PASS/FAIL line per invariant; exit 1 on any failure | `blue_line.invariants_hold` |
| `gen_formalism_ledger.py` | Regenerates `data/formalism_claim_ledger.json` from the live package; the file is a derived projection, never edited by hand | `blue_line.ledger.write_formalism_ledger` |
| `read_file_cli.py` | Reads a strict JSON declaration; optional `--as-of YYYY-MM-DD` defaults to current local date. Exposes effective context, findings, surfaces, replay report and declaration worklist; malformed shape is exit 2 | `blue_line.cli.read_file_main` |
| `gen_examples.py` | Regenerates local prepared envelopes, companion reports and bindings; preserves historical subject references | `blue_line.examples.write_examples` |
| `check_publication.py` | Checks local version agreement, not DOI identity or external publication | `blue_line.publication.check_publication_main` |
| `render_manuscript.py` | Hydrates variables and invokes PDF/HTML rendering in an explicitly supplied isolated template export | template rendering APIs |
| `build_manuscript_bundle.py` | Packages the complete web asset tree, figures and PDF after rendering | `blue_line.publication.build_manuscript_bundle` |

Do not add business, data, or plot logic to scripts; put it in
`src/blue_line/` and delegate.
