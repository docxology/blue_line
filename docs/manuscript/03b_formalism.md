# Formalism

## Definitions

::: {#def:reading}
A **reading** contains file verdict $v$, findings $F$, intake transcript $N$,
review diagnostics $Q$, resolved date $d$, registry digest $g$ and version,
normalized declaration, and versioned evaluation context. The context binds
normalized-input identity, effective window, unknown-tag policy and evaluator
version. The legacy projection is a proper subset of this record.
:::

::: {#def:commitment}
A **commitment** is a record $c = (i, t, w, T, S, k)$ with id $i$, title
$t$, wire $w$, tag set $T$, ordered required signals $S = (s_1, \ldots, s_m)$,
and kind $k$.
:::

::: {#def:fresh-set}
The **fresh set** $A_d$ at review date $d$ is the set of declared signal
labels that are either undated or dated $d'$ with $0 \le d - d' \le W$,
where $W$ is the freshness window.
:::

The raw stale set $B_d$ contains labels with a declaration older than $W$.
It may overlap $A_d$: a fresh renewal does not erase declared history.
For required labels $S$, define missing labels $M = S \setminus A_d$ and
effective stale labels $E = S \cap (B_d \setminus A_d)$.

## Properties

::: {#prop:fail-closed}
**Fail-closed property.** If no commitment applies to the declared file,
the verdict is OUTSIDE_SCOPE and $F$ is empty. An empty scan never
yields MAINTAINED.
:::

::: {#prop:staleness-monotone}
**Effective stale subset.** $E \subseteq M$. Raw stale membership alone does
not imply missing membership. A fresh dated or undated renewal takes precedence.
Future-dated records are excluded at review and diagnosed separately from
unreadable dates set aside during intake.
:::

::: {#prop:digest-pinning}
**Digest pinning.** Every reading carries the registry digest $g$
computed from ordered canonical registry content, with unordered fields sorted.
Different content is expected to produce different SHA-256 hashes under ordinary
cryptographic collision-resistance assumptions; collision impossibility is not
claimed. Projection equality can arise deliberately for different input or policy.
Replay identity binds those additional contexts, not truth or authenticity.
:::
