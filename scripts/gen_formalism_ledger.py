"""Generate data/formalism_claim_ledger.json from the live package.

Every entry is derived at run time from the registry, the evaluator surface,
and the figure specs. Nothing is hardcoded; the ledger is a projection of
what the package actually exposes, stamped with the registry digest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line.ledger import write_formalism_ledger  # noqa: E402


def main() -> int:
    out = write_formalism_ledger(Path(__file__).resolve().parents[1])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
