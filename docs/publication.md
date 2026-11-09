# Publication and versioned releases

## Source citation and archive objects

Source edition **0.3.2**, dated November 9, 2026. Cite inspected source
through <https://github.com/docxology/blue_line> with its version and exact revision.
A source declaration, GitHub Release, source archive, and rendered manuscript
are separate objects; each needs its own publication and qualification evidence.

Previously verified source archive: **0.3.1** /
<https://doi.org/10.5281/zenodo.24069451>. That identifier names the released
SOURCE ZIP only, not this later source or a standalone rendered manuscript.
The retained older title/DOI reference (`10.5281/zenodo.22833490`) remains
historical; its exact edition version is not established here. Later source
is cited by repository until its exact edition/object is independently verified.

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

The owner authorized the November 8, 2026 GitHub Release campaign with the
existing public repositories' Zenodo hooks left active. That is dated authority,
not a receipt for this candidate or blanket future authorization. For a future
owner-authorized release, inspect authenticated hooks immediately before
publication, retain the authorized integration, and independently verify each
resulting archive's repository, tag, version, and contents. Normal authorized
GitHub Release plus the existing public hook remains allowed. Manual reserve-first
is an alternative for a specifically authorized object, not a universal
prerequisite; a reserved DOI is not a published deposit.

Until its actual record is verified, no new DOI is asserted. Keep previously
verified identifiers assigned to their historical versions. Never guess a DOI
or amend an immutable tag to insert one learned afterward. Without explicit
archive-publication authority, a Zenodo hook or inconclusive hook observation
still blocks a Release object. PyPI publication, private-source disclosure, and
new deposit automation for private siblings remain unauthorized.
