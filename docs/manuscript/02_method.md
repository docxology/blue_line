# Method

## Registry

The registry lists commitments, each a frozen record with an id, a
title, a wire (the practice in one sentence), applicable tags from a
reviewed vocabulary, an ordered tuple of required care signals, and a kind
family (system, obligation, relationship, artifact). The registry digest is
the SHA-256 of ordered canonical content: commitment and required-signal tuple
order is preserved; vocabulary and tag sets are sorted. Every reading pins
the digest of the registry that produced it. Universal shape validation is
shared by runtime and the registry checker; canonical size and kind policy
are additional checks, not requirements for small custom registries.

## Staged intake

Reading is staged. Intake first normalizes the declared file: descriptions
must be non-blank text; tags and evidence labels are stripped, lowercased,
and tags are matched against the vocabulary; dated care signals must carry ISO
dates or they are set aside with notes. JSON shapes are checked before immutable
records are built; malformed JSON declarations are usage errors. Library intake
sets aside unsupported containers without coercion. No token is stringified into
a positive declaration. Unknown-tag tolerance remains an explicit policy.
Accepted library date spellings are normalized to calendar-date form before
input hashing and replay; the JSON boundary requires that canonical form.

## Evaluation

Applicable commitments are those sharing at least one tag with the declared
file. For each, the evaluator compares required signals with the fresh set
— undated declarations plus dated ones inside the freshness window ({{FRESHNESS_WINDOW_DEFAULT_DAYS}}
days by default, configurable). All fresh yields MAINTAINED; some missing
yields NEEDS_ATTENTION; a missing signal that aged past the window yields
STALE. Per-commitment surfaces keep present, missing, and stale co-present
so the projection is recoverable.

One staged declaration and one resolved date/window produce both findings and
surfaces. Fresh declarations take precedence over stale declarations of the same
label. Future-dated records do not count as fresh and receive review diagnostics,
separate from unreadable-date intake notes. Omitted CLI dates use the current
local date; explicit dates support replay. Every successful CLI read exposes
the effective policy and registry identity.

The legacy reading hash identifies a coverage projection, not source identity.
A versioned companion report binds normalized input, effective policy, evaluator
version, review date and registry version in a replay digest. Replay recomputes
the staged evaluation and preserves the intake transcript; it neither recovers
discarded input nor verifies original file bytes, references or authenticity.
The shared envelope retains its field set and legacy projection reference;
only applicable readings with complete identity are eligible for construction.
Subject-bound envelope identity is separate from report-content identity.

![Registry commitments grouped by kind with required declaration labels.](../../output/figures/blue_registry_map.png){#fig:blue-registry-map}

![Declared signal coverage resolves to the unchanged verdict vocabulary.](../../output/figures/blue_verdict_paths.png){#fig:blue-verdict-paths}

![Freshness policy with renewal precedence and separate future-date diagnostics; the date is a historical example.](../../output/figures/blue_freshness_window.png){#fig:blue-freshness-window}

## Fail-closed semantics

An empty scan set — no commitment matches, or the file cannot be read —
returns OUTSIDE_SCOPE with notes. Absence of siblings, of signals, and of
input are all outcomes, never exceptions or fabricated values.
