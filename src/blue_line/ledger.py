"""The formalism claim ledger as a derived projection of the live package.

Every entry is built at run time from the registry, the evaluator surface,
and the figure specs. Nothing is hardcoded; the ledger is a projection of
what the package actually exposes, stamped with the registry digest. It
records what the package exposes; it does not establish that any
commitment is in fact maintained, correct, or available.

``scripts/gen_formalism_ledger.py`` is the thin wrapper around
:func:`write_formalism_ledger`.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .enums import CommitmentKind, FileStatus, StewardshipStatus
from .figures import FIGURE_SPECS
from .registry import BLUE_COMMITMENTS
from .serialization import canonical_registry, registry_digest

LEDGER_SCHEMA = "blue_line.formalism-claim-ledger/1.0"


def build_formalism_ledger() -> dict:
    """Build the ledger payload from the live package, digest included."""

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
        "schema": LEDGER_SCHEMA,
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
    return payload


def write_formalism_ledger(repo: Path) -> Path:
    """Build the ledger and write it to ``repo/data/formalism_claim_ledger.json``.

    Returns the written path.
    """

    out = Path(repo) / "data" / "formalism_claim_ledger.json"
    payload = build_formalism_ledger()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + chr(10), encoding="utf-8")
    return out
