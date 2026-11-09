# Declaration, evaluation and transport contracts

The CLI's `blue_line.cli/2.0` object retains verdict, findings and surfaces and
adds resolved date, effective window, registry identity, review diagnostics,
companion report and worklist. Its omitted-date policy is current local date;
historical examples always pass a date explicitly. The library accepts a
`datetime.date` or an ISO date string, including basic/week spellings, or defaults
to the current local date; `datetime.datetime` is not a review date. The date and
window are resolved once, and one normalized declaration produces findings and
surfaces.

Pass a reading and the surfaces returned with it by the **same**
`read_with_surfaces` call to `build_report` or `stewardship_worklist`. These
projectors neither re-evaluate nor validate that independently supplied pairs
belong together; `replay_report` separately checks complete correspondence.

JSON input requires an object. Label fields require arrays of nonblank text;
dated evidence requires an array of objects with a text label and optional ISO
date or null. Unknown fields, malformed shapes and malformed dates are usage
errors. Diagnostics identify field and index without converting tokens to text.
Library intake supports label lists, tuples, sets and frozensets, and dated-record
lists or tuples. Mappings, strings, null containers and iterators are set aside
without consumption or coercion. Malformed tokens become deterministic notes.
Accepted ISO basic/week dates in library records are normalized to calendar-date
spelling before input hashing, so their staged reports can pass the strict JSON
replay boundary. CLI `--as-of`, JSON signal dates and `declared_next_review`
require canonical `YYYY-MM-DD` spelling. Invalid calendar dates and ISO basic/week
spellings for `--as-of` return exit 2, a diagnostic on stderr and no stdout.
The existing unknown-tag tolerance remains explicit (`allow_unknown_tags`);
strict mode blocks unknown tags. Custom registries use the built-in vocabulary.
Unsupported custom tags are registry errors, not silently unmatched scans.

Universal registry validation checks record shape, unique nonblank IDs, titles,
wires, supported tags, unique canonical signal labels and enum kinds. The registry
checker adds the canonical size and kind-coverage policies; small valid custom
registries remain usable through the library. Empty registries fail closed as
OUTSIDE_SCOPE. Declaration order and required-signal order remain semantic:
the published registry digest is unchanged and binds ordered content; vocabulary
and tag sets are sorted before hashing.

`reading_digest` remains the legacy projection hash. It intentionally omits input,
effective policy and registry version. Distinct declarations with equivalent
coverage can share it. This is projection equality, not a cryptographic collision.
`blue_line.evaluation-context/1.0` binds the normalized-input hash, resolved date,
effective window, unknown-tag policy and package/evaluator version.
`blue_line.replay/1.0` binds that context, registry version, projection and review
diagnostics. Version changes must change replay identity even for the same verdict.

`blue_line.report/1.0` carries normalized input, context and its digest, registry
version, legacy projection and its digest, replay digest, review notes and surfaces.
`replay_report` re-evaluates the staged declaration against a supplied matching
registry and the current matching evaluator version, and compares the whole report.
Original intake diagnostics are retained as a transcript: replay does not recover
discarded tokens, validate those diagnostics independently, bind original file
bytes, or establish authenticity. Normalization-equivalent inputs intentionally
share input identity. Input changes that survive normalization, including description
and declared metadata, change input identity even if coverage stays unchanged.
Unsupported schemas and evaluator versions are rejected; there is no silent
migration. Historical projection semantics are preserved, while prepared examples
are intentionally regenerated with current version and companion reports.

Prepared example generation reads declarations and `data/example_contexts.json`,
never previous envelopes or reports. Contexts are maintained inputs; generated
outputs can be removed or corrupted and rebuilt with identical bytes. Historical
release packets remain archived; replay of an older evaluator version requires
that evaluator rather than relabeling the stored report.
Generation refreshes only currently declared file stems; it does not retire old
output filenames. The authored declaration set, not a directory listing of
generated reports, is the current example roster.

`line.report-envelope/1.0` keeps its shared field set. Only applicable readings
with findings and complete date, registry and context identity can be built;
the helper and builder enforce the same eligibility. A normalized unmatched
OUTSIDE_SCOPE reading can retain a local report. Blocked intake has no normalized
declaration: `build_report` refuses it and the CLI emits `report: null`.
Neither case is eligible for an envelope.
NEEDS_ATTENTION and STALE remain recordable. `report_ref` remains the precisely
named legacy projection digest; a companion report adds replay context without
altering the shared schema. `envelope_digest` identifies the entire envelope,
including subject and sorted snapshot references, separately from report content.
Identifiers and snapshot references are declarations, not inspected content.

The worklist is a sorted projection of missing/stale surfaces, with commitment ID,
signal, declaration status and optional file-level declared owner, next-review
date and source reference. Missing metadata stays null. It synthesizes no health
score, priority, due date, obligation or availability promise. Undated evidence
still counts as current by declared policy. Fresh renewals override stale history;
future-dated evidence is excluded at review with separate review diagnostics.
