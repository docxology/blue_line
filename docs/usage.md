# Read a commitment declaration

Install uv and sync the locked environment from the repository root. The package supports Python 3.11 and newer. The checkout selects Python 3.15.

```sh
uv sync --locked
uv run --locked python scripts/read_file_cli.py --as-of 2026-11-09 \
  '{"description":"Service handbook","tags":["docs"],"evidence":["handover_note"]}'
```

Change the description, tags and evidence to match your declaration. Evidence labels and dated care signals describe steward declarations. Use the [declaration schema and intake policy](reports.md) to add dated signals, a declared owner, a next review date or a source reference.

Pass a `YYYY-MM-DD` review date for reproducibility. The CLI uses the local current date when the option is omitted. Its JSON includes the effective freshness window, registry identity, verdict and per-commitment signal surfaces. Malformed date or JSON syntax returns exit code 2 and a diagnostic on standard error.

| Verdict | Meaning at the resolved review date |
| --- | --- |
| MAINTAINED | Every required signal for the applicable commitments is freshly declared. |
| NEEDS_ATTENTION | Required signals are missing and the file has no stale findings. |
| STALE | An applicable required signal is missing and an older declaration aged past the freshness window. |
| OUTSIDE_SCOPE | The read produced an empty applicable commitment set. |

Use the [claim register](claim_boundaries.md) to interpret the verdict and the [report contract](reports.md) to reproduce the reading or prepare an envelope.

[Documentation index](README.md)
