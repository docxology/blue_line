"""Registry content, ordering, and invariants."""

from __future__ import annotations

import blue_line
from blue_line.enums import CommitmentKind
from blue_line.evaluator import invariants_hold
from blue_line.registry import BLUE_COMMITMENTS, COMMITMENT_TAG_VOCABULARY, registry_ids


def test_registry_has_at_least_six_entries():
    assert len(BLUE_COMMITMENTS) >= 6


def test_registry_ids_match_declaration_order():
    assert registry_ids() == tuple(c.id for c in BLUE_COMMITMENTS)


def test_registry_ids_distinct():
    ids = registry_ids()
    assert len(ids) == len(set(ids))


def test_all_tags_in_vocabulary():
    for commitment in BLUE_COMMITMENTS:
        assert commitment.tags <= COMMITMENT_TAG_VOCABULARY


def test_kinds_cover_at_least_three_families():
    kinds = {c.kind for c in BLUE_COMMITMENTS}
    assert len(kinds) >= 3


def test_every_kind_member_is_enum():
    for commitment in BLUE_COMMITMENTS:
        assert isinstance(commitment.kind, CommitmentKind)


def test_required_signals_nonempty_and_ordered():
    for commitment in BLUE_COMMITMENTS:
        assert commitment.required_signals
        assert len(commitment.required_signals) == len(set(commitment.required_signals))


def test_invariants_hold_on_canonical_registry():
    results = invariants_hold()
    failed = [name for name, passed, _ in results if not passed]
    assert failed == []


def test_invariants_fail_on_duplicate_registry():
    doubled = BLUE_COMMITMENTS + (BLUE_COMMITMENTS[0],)
    results = blue_line.invariants_hold(doubled)
    by_name = dict((name, passed) for name, passed, _ in results)
    assert by_name["distinct_commitment_ids"] is False


def test_invariants_fail_on_small_registry():
    results = blue_line.invariants_hold(BLUE_COMMITMENTS[:2])
    by_name = dict((name, passed) for name, passed, _ in results)
    assert by_name["min_registry_size"] is False
