"""Command bodies for the thin orchestrator scripts in ``scripts/``.

Each function here is the full behavior of one script entrypoint so the
script itself stays a path bootstrap plus a single delegated call. These
bodies parse arguments, print, and return exit codes; the reading logic
they invoke lives in :mod:`blue_line.evaluator`. They report readings and
verdicts; they do not establish maintenance, correctness, or availability.
"""

from __future__ import annotations

import json
import sys
from datetime import date

from .evaluator import DEFAULT_MAX_SIGNAL_AGE_DAYS, read_with_surfaces
from .json_adapter import DeclarationShapeError, declaration_from_json
from .report import build_report, stewardship_worklist


def read_file_main(argv: list[str] | None = None) -> int:
    """Read one declared commitment file described as JSON on argv.

    The JSON object mirrors CommitmentFile fields (description, tags,
    evidence, dated_evidence). Prints the verdict and per-commitment
    findings as JSON. Returns 2 on usage or JSON errors, 0 on success.
    """

    argv = list(sys.argv[1:] if argv is None else argv)
    as_of = None
    if "--as-of" in argv:
        index = argv.index("--as-of")
        if index + 1 >= len(argv):
            print("--as-of requires a YYYY-MM-DD value", file=sys.stderr)
            return 2
        as_of = argv[index + 1]
        try:
            parsed = date.fromisoformat(as_of)
        except ValueError:
            print(
                "--as-of requires a valid calendar date in YYYY-MM-DD form",
                file=sys.stderr,
            )
            return 2
        if parsed.isoformat() != as_of:
            print(
                "--as-of requires a calendar date in YYYY-MM-DD form", file=sys.stderr
            )
            return 2
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
    try:
        file = declaration_from_json(payload)
        reading, surfaces = read_with_surfaces(file, as_of=as_of)
    except (DeclarationShapeError, ValueError) as error:
        print(f"invalid declaration: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "schema_version": "blue_line.cli/2.0",
                "status": reading.status.value,
                "read_as_of": reading.read_as_of,
                "max_signal_age_days": DEFAULT_MAX_SIGNAL_AGE_DAYS,
                "registry_version": reading.registry_version,
                "registry_digest": reading.registry_digest,
                "report": build_report(reading, surfaces)
                if reading.normalized_input is not None
                else None,
                "worklist": stewardship_worklist(reading, surfaces),
                "intake_notes": list(reading.intake_notes),
                "review_notes": list(reading.review_notes),
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
            sort_keys=True,
        )
    )
    return 0
