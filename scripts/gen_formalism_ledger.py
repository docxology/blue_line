"""Generate data/formalism_claim_ledger.json from the live package.

Every entry is derived at run time from the registry, the evaluator surface,
and the figure specs. Nothing is hardcoded; the ledger is a projection of
what the package actually exposes, stamped with the registry digest.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line import (  # noqa: E402
    CommitmentKind,
    FileStatus,
    StewardshipStatus,
)
from blue_line.figures import FIGURE_SPECS  # noqa: E402
from blue_line.registry import BLUE_COMMITMENTS  # noqa: E402
from blue_line.serialization import canonical_registry, registry_digest  # noqa: E402


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    registry_digest_value = registry_digest()
    commitments = [
        {
            "id": c.id,
            "kind": c.kind.value,
            "title": c.title,
            "wire": c.wire,
            "tags": sorted(c.tags),
            "required_signals": list(c.required_signals),
        }
        for c in BLUE_COMMITMENTS
    ]
    payload = {
        "schema": "blue_line.formalism-claim-ledger/1.0",
        "registry_digest": registry_digest_value,
        "registry_canonical": canonical_registry(),
        "commitments": commitments,
        "kinds": sorted(k.value for k in CommitmentKind),
        "file_verdicts": sorted(v.value for v in FileStatus),
        "commitment_verdicts": sorted(v.value for v in StewardshipStatus),
        "figures": [
            {"figure_id": s.figure_id, "title": s.title, "description": s.description}
            for s in FIGURE_SPECS
        ],
        "ledger_digest": "",
    }
    digestable = {k: v for k, v in payload.items() if k != "ledger_digest"}
    body = json.dumps(digestable, sort_keys=True).encode("utf-8")
    payload["ledger_digest"] = hashlib.sha256(body).hexdigest()
    out = repo / "data" / "formalism_claim_ledger.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + chr(10), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
