"""Thin CLI: run the registry invariants and print the battery."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line import invariants_hold  # noqa: E402


def main() -> int:
    results = invariants_hold()
    failed = 0
    for name, passed, detail in results:
        mark = "PASS" if passed else "FAIL"
        print(f"{mark}  {name}{'  ' + detail if detail and not passed else ''}")
        failed += 0 if passed else 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
