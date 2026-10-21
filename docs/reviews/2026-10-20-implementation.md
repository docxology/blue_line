# Review implementation disposition

Source: the complete received review packet, reviewed against `fc7bde7`.
Its body hash was verified against the supplied manifest after excluding the
packet wrapper's single appended newline. The packet's counterexamples were
proposals; the executions below are this run's evidence. All items are resolved
within blue_line. No sibling was modified.

Every item below, including the confirmed independent-audit corrections, is
implemented in commit `6b8b2ae7e600f6095e8a921a4cf5d98da97dea0f`. The release follow-up
commit records independent approval and the final verification disposition.

| Item | Disposition and implementation | Executed regression evidence |
| --- | --- | --- |
| BL-01 | Done: current local date by default, explicit historical replay, resolved date/window/version/digest in every successful CLI output. | New boundary tests failed on absent output identity; explicit historical dates produced the proposed different verdicts. Inclusive freshness-boundary tests already passed and retain that behavior. |
| BL-02 | Done: strict object/array/record adapter with field/index errors; malformed CLI shape exits as usage error. Library mappings and iterators are unsupported and set aside without consumption or coercion. | Shape tests raised AttributeError/TypeError or returned success before the fix. Both false- and true-valued evidence objects returned MAINTAINED before the fix; both now fail at the CLI boundary and cannot declare evidence in the library. |
| BL-04 | Done: one intake, one resolved date/window, one per-commitment calculation supplies findings and surfaces. Iterators are explicitly rejected, as permitted by the proposal. | A supported list's real iteration counter observed duplicate intake before the refactor and one pass afterward. Iterator rejection preserves its unconsumed values. Finding/status and surface partition controls agree. |
| BL-05 | Done: shared universal validator; optional canonical size/kind policy. Custom registries retain small-registry support but use the built-in tag vocabulary. | Blank title/ID, empty/duplicate/noncanonical signals passed the old checker; malformed kind crashed it; unsupported custom tags reached ordinary evaluation. The matrix now returns deterministic diagnostics and runtime fails closed. Existing correctly rejected cases remain covered. |
| BL-03 | Done, with explicit identity boundary: preserve and name the published legacy projection digest; add versioned normalized-input/context/replay identity, companion reports and envelope bindings. | The effective-policy/input test failed because context was absent. JSON round-trip now reproduces reading and surfaces; policy/version/source mutations distinguish identity even where projection equality is intentional. Mutated report and schema controls reject. |
| BL-06 | Done: applicable readings only, complete identity and nonblank subject/reference identifiers, typed eligibility error. Shared field set preserved. | Direct builder controls for blocked intake, malformed registry and incomplete identity all succeeded incorrectly before the fix. They now reject. Prepared envelopes reproduce and the available sibling schema field test passes. Separate live sibling intake accepted both prepared envelopes without issues. |
| BL-07 | Done: effective stale is required intersect (raw stale minus fresh); future-only declarations have separate review diagnostics; collision impossibility removed. | Renewal tests already passed: no semantics change was needed. The missing future-review diagnostic test failed before the fix. Invalid-date intake remains distinct; stale surfaces remain a subset of missing. |
| BL-08 | Adapted as explicitly offered: retain ordered registry hashing; cover is symbolic, not a registry chart. Freshness labels derive from the effective policy; PNG provenance records renderer and environment. | Reordered registry identity already differed, confirming the published ordered contract. Configured freshness-label and missing renderer-receipt tests failed before the fix. Same-environment PNG bytes remain stable. |
| Worklist proposal | Done: sorted missing/stale declaration rows with optional file-level declared owner, next-review date and source reference; no priority, health score or inferred deadline. | Worklist rows equal the evaluator's missing surfaces, optional metadata is retained, absent metadata stays null, and malformed metadata is rejected or set aside at its boundary. |

No finding is silently dropped. Existing working behavior (freshness inclusivity,
renewal precedence and ordered hashing) is retained with executed evidence rather
than changed to make a proposal appear implemented. The optional dated-only policy
was not introduced: the proposal only requires recording such a mode if introduced;
the documented undated-current policy is preserved.

## Contract adaptations

- The required publication document was absent. Added guidance records this brief's
  reserve-first procedure and preserves the previously verified DOI as historical.
- The runtime stays standard library only and development dependencies stay within
  the repository contract. Generic skill library defaults do not override it.
- Replay binds normalized declarations and retains intake notes as a transcript;
  it does not recover discarded tokens or bind original source bytes. Blocked
  intake remains a local reading, not a fabricated replayable source record.
- OUTSIDE_SCOPE remains locally recordable but ineligible for a shared envelope.
- The projection hash remains compatible. Companion report bindings supply replay
  context without expanding the agreed flat envelope schema.
- Original source-reference and other-instrument version strings in historical
  prepared subjects remain historical, rather than being relabeled as new evidence.

## Rendering evidence and cross-repository findings

The isolated template export is from its recorded origin/main commit. Initial SVG
embeds failed LaTeX's Inkscape export requirement. Switching this project's embeds
to generated PNGs exposed an honest registry mismatch; the new negative test
reproduced it, and rasterization now updates the figure registry to the emitted
file. Both failed logs are retained locally; the final PDF/HTML gate passes without
an engine modification or a suppressed failure.

Witness Register maintainers should consume Blue's companion report binding when
they need normalized-input/policy replay identity: the legacy `report_ref` identifies
a coverage projection. Schema admission is shape acceptance, not replay or truth.
Historical Blue envelopes copied into siblings are not updated by this release;
their maintainers must deliberately decide whether and how to refresh them.
No cross-repository code change is needed for the existing flat field set.

Daniel must reserve and mint the new Zenodo version DOI. A new GitHub Release
object is permitted only by a fresh conclusive no-Zenodo-webhook check.
