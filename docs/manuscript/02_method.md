# Method

## Registry

The registry lists twelve commitments, each a frozen record with an id, a
title, a wire (the practice in one sentence), applicable tags from a
reviewed vocabulary, an ordered tuple of required care signals, and a kind
family (system, obligation, relationship, artifact). The registry digest is
the SHA-256 of the sorted canonical form; every reading pins the digest of
the registry that produced it.

## Staged intake

Reading is staged. Intake first normalizes the declared file: descriptions
must be non-blank text; tags and evidence labels are stripped, lowercased,
and matched against the vocabulary; dated care signals must carry ISO dates
or they are set aside with notes. Nothing crashes and nothing is invented:
every ignored token becomes an intake note the declarer can read.

## Evaluation

Applicable commitments are those sharing at least one tag with the declared
file. For each, the evaluator compares required signals with the fresh set
— undated declarations plus dated ones inside the freshness window (180
days by default, configurable). All fresh yields MAINTAINED; some missing
yields NEEDS_ATTENTION; a missing signal that aged past the window yields
STALE. Per-commitment surfaces keep present, missing, and stale co-present
so the projection is recoverable.

## Fail-closed semantics

An empty scan set — no commitment matches, or the file cannot be read —
returns OUTSIDE_SCOPE with notes. Absence of siblings, of signals, and of
input are all outcomes, never exceptions or fabricated values.
