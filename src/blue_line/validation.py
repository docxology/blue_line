"""Shared registry shape and optional canonical policy checks; no care is verified."""

from __future__ import annotations

from .enums import CommitmentKind
from .records import Commitment
from .registry import COMMITMENT_TAG_VOCABULARY


def registry_shape_error(commitments: tuple[Commitment, ...]) -> str | None:
    if not isinstance(commitments, tuple):
        return "commitment registry must be a tuple"
    seen: set[str] = set()
    for index, commitment in enumerate(commitments):
        if not isinstance(commitment, Commitment):
            return f"commitment registry entry {index} is not a Commitment record"
        if any(not isinstance(v, str) or not v.strip() for v in (
            commitment.id, commitment.title, commitment.wire
        )):
            return f"commitment registry entry {index} has blank or non-text fields"
        if commitment.id != commitment.id.strip():
            return f"commitment registry entry {index} has a noncanonical id"
        if commitment.id in seen:
            return f"commitment registry contains duplicate id '{commitment.id}'"
        seen.add(commitment.id)
        if (not isinstance(commitment.tags, frozenset) or not commitment.tags
            or any(not isinstance(t, str) or not t.strip() for t in commitment.tags)):
            return f"commitment '{commitment.id}' has malformed tags"
        if not commitment.tags <= COMMITMENT_TAG_VOCABULARY:
            return f"commitment '{commitment.id}' has unsupported tags: {sorted(commitment.tags - COMMITMENT_TAG_VOCABULARY)}"
        signals = commitment.required_signals
        if (not isinstance(signals, tuple) or not signals
            or any(not isinstance(s, str) or not s.strip() for s in signals)):
            return f"commitment '{commitment.id}' has malformed required signals"
        if any(s != s.strip().lower() for s in signals) or len(set(signals)) != len(signals):
            return f"commitment '{commitment.id}' requires unique canonical signal labels"
        if not isinstance(commitment.kind, CommitmentKind):
            return f"commitment '{commitment.id}' has an invalid kind"
    return None


def validate_registry(
    commitments: tuple[Commitment, ...], *, canonical: bool = False,
) -> tuple[tuple[str, bool, str], ...]:
    """Universal rules apply to all registries; size and kind policy are opt-in."""
    error = registry_shape_error(commitments)
    results = [("registry_shape", error is None, error or "")]
    results.append(("distinct_commitment_ids", error is None or "duplicate id" not in error, error or ""))
    if canonical and error is None:
        results.append(("min_registry_size", len(commitments) >= 6, f"{len(commitments)} entries"))
        kinds = sorted({c.kind.value for c in commitments})
        results.append(("kind_coverage", len(kinds) >= 3, f"kinds: {kinds}"))
    return tuple(results)
