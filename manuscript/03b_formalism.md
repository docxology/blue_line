# Formalism

## Definitions

::: {#def:reading}
A **reading** is a tuple $R = (v, F, N, d, g)$ where $v$ is the file
verdict, $F$ is a tuple of commitment findings, $N$ is a tuple of intake
notes, $d$ is the review date, and $g$ is the registry digest.
:::

::: {#def:commitment}
A **commitment** is a record $c = (i, t, w, T, S, k)$ with id $i$, title
$t$, wire $w$, tag set $T$, ordered required signals $S = (s_1, dots, s_m)$,
and kind $k$.
:::

::: {#def:fresh-set}
The **fresh set** $A_d$ at review date $d$ is the set of declared signal
labels that are either undated or dated $d'$ with $0 le d - d' le W$,
where $W$ is the freshness window.
:::

## Properties

::: {#prop:fail-closed}
**Fail-closed property.** If no commitment applies to the declared file,
the verdict is $v = $ OUTSIDE_SCOPE and $F$ is empty. An empty scan never
yields MAINTAINED.
:::

::: {#prop:staleness-monotone}
**Staleness monotonicity.** If a signal label is in the stale set at date
$d$, it is in the missing set for every commitment requiring it; stale is
always a subset of missing.
:::

::: {#prop:digest-pinning}
**Digest pinning.** Every reading carries the registry digest $g$
computed from the sorted canonical registry; two readings with different
registry content cannot share a digest.
:::
