# Blue Line runtime modules

Runtime package. Pure standard library, frozen dataclasses, no mocking.

| Module | Contents |
|--------|----------|
| `__init__.py` | Public API re-exports (`blue_line.__all__`) |
| `enums.py` | Verdict, file-status and commitment-kind enumerations |
| `records.py` | Frozen record types for commitments, declared files, readings and surfaces |
| `registry.py` | Versioned commitment registry, tag vocabulary, ID listing |
| `validation.py` | Shared registry shape checks plus optional canonical size/kind policy |
| `intake.py` | Fail-closed staged intake: set-asides with notes, never exceptions or invented values |
| `json_adapter.py` | Strict JSON shape boundary for CLI input |
| `evaluator.py` | Staged evaluation, verdict function, registry invariants |
| `serialization.py` | Canonical serialization and derived digests (registry, reading, context, replay) |
| `report.py` | Versioned replay reports and the declaration worklist |
| `envelope.py` | `line.report-envelope/1.0` construction and eligibility |
| `ledger.py` | Formalism claim ledger derived from the live package |
| `examples.py` | Regenerates prepared declarations, envelopes and companion reports under `data/` |
| `publication.py` | Local version consistency checks and manuscript bundle packaging; DOI identity and external publication are separate |
| `cli.py` | Command bodies for the thin `scripts/` entrypoints |
| `version.py` | Package version marker |
| `figures/` | Deterministic figure specs, SVG/PNG builders |

See the [report contract](../reports.md) and [claim register](../claim_boundaries.md)
for behavior. The supporting guides cover [figures](figures.md),
[data](data.md), [envelopes](envelopes.md) and [verification](verification.md).
