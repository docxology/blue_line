# Independent pre-tag audit and resolutions

The independent auditor ran read-only against the full candidate diff from
`fc7bde7`, using the complete review packet. It did not build this work or modify
any source, sibling, engine, artifact or Git state.

Initial disposition: **REQUEST CHANGES; do not tag**.

| Finding | Confirmed reproduction | Resolution |
| --- | --- | --- |
| P1: accepted library ISO basic/week dates cannot replay | A reading retaining compact/week date spelling builds a report that the strict JSON adapter rejects. | Normalize every accepted library signal date before storing the staged input; regression tests exercise basic, week and calendar forms through JSON round-trip. |
| P2: envelope eligibility accepts invalid policy | Negative freshness windows and nonboolean unknown-tag policy pass the helper and builder while report replay rejects them. | Validate complete policy shape and bounds in the eligibility helper; helper and typed builder rejection tests cover malformed policy fields. |
| P2: canonical registry checker crashes on nonsized input | `invariants_hold(None)` reaches `len` after a shape error. | Canonical size/kind checks run only after universal shape succeeds; null, scalar and iterator controls now fail closed. |
| P2: distributed ZIP omits referenced local assets | Local HTML uses a font loader and favicon absent from the original ZIP. | A tested package function includes the entire web asset tree, figures and PDF; the refreshed extracted bundle receives byte/CRC and browser checks. |

The root reproduced the findings with failing regressions before applying the
fixes. The auditor also independently confirmed manifest byte/hash closure,
prepared replay/bindings, ledger and freshness producers, unchanged claim
boundaries, cache-free lint, whitespace, current gate receipts and the retained
PDF/HTML visual evidence. It accepted the disclosed projection hash, retained
intake transcript, previous DOI and error-severity type-check boundaries.

Audit task ID:
`node:delegated-task:command%3Amcp%3Ace05f7af-2b27-4aa0-957f-965bde40aeb4%3Adelegate-task%3Ablue-line-v020-pretag-audit-20261021-round1`.

Focused independent recheck of the corrected complete candidate is pending;
tagging remains blocked until that receipt is recorded.
