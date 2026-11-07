# AGENTS.md — `blue_line/docs/releases`

## Scope
- Historical release packets, not a live report of the current checkout.
  Current changes belong in the root `CHANGELOG.md` under Unreleased.

## Layout
- `v0.1.0.md` and `v0.2.0.md` retain the evidence recorded for those releases.
- `v0.2.0-artifacts.json` retains the versioned artifact manifest.
- `README.md` explains the release-note convention.

## Gotchas
- Preserve published gate results, counts, source identities and checksums.
  Do not regenerate these packets when refreshing current examples or figures.
- A new release packet requires actual run evidence under `../publication.md`;
  never infer a source commit, publication, or DOI.
