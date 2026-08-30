# Changelog

## 0.1.0 — 2026-08-29

Initial release of the blue line.

- Versioned commitment registry (12 entries) with tag vocabulary and kind
  families.
- Fail-closed staged intake (set-asides with notes; strict tag mode).
- Evaluator: MAINTAINED / NEEDS_ATTENTION / STALE / OUTSIDE_SCOPE with
  per-commitment signal surfaces and registry-digest pinning.
- Canonical serialization with sorted-before-emit digests.
- Witness-register envelope builder (line.report-envelope/1.0) and prepared
  worked + same-subject envelopes under `data/`.
- line_set binding declaration under `data/binding_declaration.json`.
- Deterministic SVG figure builders (3 figures + manifest).
- Generated formalism claim ledger.
- 87 tests, 97.33% coverage, ruff clean, zero mocks.
