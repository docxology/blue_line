# Publication and versioned releases

The review dispatch referred to this file, but it was absent at the reviewed
commit. This release records the explicit reserve-first procedure from Daniel's
brief here; no missing historical procedure is inferred.

Choose a semver greater than all current declarations and remote tags. Behavior
changes require at least a minor increment. Synchronize package, pyproject/lock,
CITATION, Zenodo metadata, manuscript configuration and the manuscript's self
reference. Historical release packets, schema versions and references to another
instrument's version retain their original identities.

Regenerate ledger/manuscript variables, examples/reports and figures; run the full
suite with its coverage floor, lint, type checks, registry, ledger and publication
checks. Render PDF and HTML using a read-only export of template `origin/main`
under GitVault, without touching an active template checkout. Record the engine
commit, commands, failures, artifact checksums and visual inspection. An engine
failure blocks this release and is reported, never patched in the engine.
SVG determinism is distinct from PNG determinism: byte-identical PNG reproduction
requires matching renderer, libraries, fonts and environment. Figure builds write
a raster provenance sidecar; it does not certify a fully pinned portable runtime.

Write a dated release packet with current-run gate evidence and a CHANGELOG entry.
Obtain one independent read-only audit of the full diff against the review packet
before tagging. Commit, annotate `vX.Y.Z`, push main and tag through the GitVault
repository lease, and verify both remote refs resolve to the release commit.

Daniel reserves the new Zenodo version DOI first and mints it in a separate owner
step. Until then, retain the last verified DOI as a reference to the previous
published version, explicitly not a DOI assigned to the new release. Never guess
or pre-fill a DOI. Publication metadata retains that identifier with this boundary.
After reservation, Daniel updates the version DOI and final deposit metadata.

Create a GitHub Release object only after an authenticated repository-hooks query
conclusively shows no Zenodo webhook. A Zenodo hook or inconclusive query means
skip the object: emitting it could mint a permanent DOI outside reserve-first.
