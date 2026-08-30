# data/ — agent notes

Regenerate `formalism_claim_ledger.json` with
`uv run python scripts/gen_formalism_ledger.py` after any registry or
figure-spec change; the ledger digest is derived, never maintained by hand.
Envelopes in `envelopes/` are prepared inputs for the witness register and
line_set maintainers — never write into the sibling repos from here.
