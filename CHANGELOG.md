# Changelog

## 0.3.0 — 2026-11-06

- Generate prepared envelopes, reports and bindings from declarations and explicit
  example contexts, not previous output files. Missing or corrupted outputs can
  be rebuilt without changing subject, review date or source-reference inputs.
- Remove the obsolete registry-shape forwarding helper; use the shared validator.
- Keep live figure/provenance checks instead of cover wording and incidental
  figure-count assertions.
- Emit figure registry 2.0 with the publication engine's canonical `alt_text`
  field; retain prior registry editions only as historical artifacts.

- Require canonical `YYYY-MM-DD` calendar dates for CLI `--as-of`; invalid and
  noncanonical values return usage error 2 with stderr only. Preserve broader
  library ISO-date normalization and existing freshness and finite-input policy.
- Add direct and executable CLI date-boundary regressions and library
  normalization controls; remove wording and source-text assertions.
- Use American English in maintained prose; distinguish the declared family
  roster from source availability, apply nonclaims to every other instrument,
  and document actual envelope/release roles without stale test counts.
- Correct the cover's local color-constant documentation without changing art.
- Refresh the generated development lock for the declared Python requirement.
- Exercise generator CLIs and publication checks in isolated project copies,
  checking emitted artifacts against native records and rejecting mismatched
  publication metadata without writing into the source checkout.

## 0.2.0 — 2026-10-21

- Resolve the CLI review date deliberately and emit effective policy and registry
  identity. Reject malformed JSON shapes before constructing declarations.
- Stage intake once; derive findings and surfaces together. Share universal
  registry validation with the canonical checker.
- Add versioned normalized-input/context replay reports and subject-bound envelope
  identity; enforce envelope eligibility while preserving the shared field set
  and legacy projection digest. Regenerate prepared examples with companion bindings.
- Derive declaration-level worklists with optional declared metadata, without
  inferred deadlines or scores.
- Correct renewal formalism, future-date diagnostics and hash assumptions. Preserve
  ordered registry hashing; label the cover symbolic and derive freshness labels.
- Record rasterizer provenance and bind PNG embeds to their figure registry.
- Synchronize manuscript, figures, claim boundaries, metadata and reserve-first
  publication guidance. The retained DOI identifies the previous publication.

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
