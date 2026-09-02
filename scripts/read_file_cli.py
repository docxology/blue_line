"""Thin CLI: read one declared commitment file described as JSON on argv.

The JSON object mirrors CommitmentFile fields (description, tags, evidence,
dated_evidence). Prints the verdict and per-commitment findings as JSON.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line import CommitmentFile, read_with_surfaces  # noqa: E402
from blue_line.records import CareSignal  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    as_of = "2026-08-01"
    if "--as-of" in argv:
        index = argv.index("--as-of")
        if index + 1 >= len(argv):
            print("--as-of requires a YYYY-MM-DD value", file=sys.stderr)
            return 2
        as_of = argv[index + 1]
        argv = argv[:index] + argv[index + 2 :]
    if len(argv) != 1:
        print(
            "usage: read_file_cli.py '<json object>' [--as-of YYYY-MM-DD]",
            file=sys.stderr,
        )
        return 2
    try:
        payload = json.loads(argv[0])
    except json.JSONDecodeError as exc:
        print(f"invalid JSON: {exc}", file=sys.stderr)
        return 2
    dated = tuple(
        CareSignal(label=str(item.get("label")), noted_on=item.get("noted_on"))
        if isinstance(item, dict)
        else item
        for item in payload.get("dated_evidence", ())
    )
    file = CommitmentFile(
        description=payload.get("description", ""),
        tags=frozenset(payload.get("tags", ())),
        evidence=frozenset(payload.get("evidence", ())),
        dated_evidence=dated,
    )
    reading, surfaces = read_with_surfaces(file, as_of=as_of)
    print(
        json.dumps(
            {
                "status": reading.status.value,
                "intake_notes": list(reading.intake_notes),
                "findings": [
                    {
                        "commitment_id": f.commitment_id,
                        "status": f.status.value,
                        "reasons": list(f.reasons),
                    }
                    for f in reading.findings
                ],
                "surfaces": [
                    {
                        "commitment_id": s.commitment_id,
                        "present": list(s.present),
                        "missing": list(s.missing),
                        "stale": list(s.stale),
                    }
                    for s in surfaces
                ],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
