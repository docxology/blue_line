# AGENTS.md — `blue_line/docs`

## Scope
- Committed documentation for this standalone repo (GitHub `docxology/blue_line`);
  no dependency on a sibling checkout or a local-only path.
- `claim_boundaries.md` is the register of record for what may and may not be
  claimed; file inventory in `README.md`.

## Layout
- Contract and procedure docs at this level (`reports.md`, `development.md`,
  `publication.md`, `extensibility.md`, `claim_boundaries.md`), plus
  `manuscript/`, `releases/` and `reviews/`.

## Gotchas
- Documented commands must stay runnable: they are exercised by the suite
  (`scripts/*.py`, `uv run pytest`, `uv run ruff check src tests scripts`).
- Do not hardcode derived numbers or digests in prose; they are generated from
  the live package and checked by test.
