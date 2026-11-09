from dataclasses import replace

import pytest

from blue_line.evaluator import invariants_hold, read_with_surfaces
from blue_line.records import CommitmentFile
from blue_line.registry import BLUE_COMMITMENTS


@pytest.mark.parametrize(
    "changes",
    [
        {"id": ""},
        {"title": ""},
        {"wire": ""},
        {"required_signals": ()},
        {"required_signals": ("x", "x")},
        {"required_signals": (" X ",)},
        {"tags": frozenset({"quantum"})},
        {"tags": frozenset({"CODE"})},
        {"tags": "code"},
        {"kind": "SYSTEM"},
    ],
)
def test_registry_checker_and_runtime_reject_same_shape(changes):
    registry = (replace(BLUE_COMMITMENTS[0], **changes),) + BLUE_COMMITMENTS[1:]
    checks = invariants_hold(registry)
    assert any(not ok for _, ok, _ in checks)
    reading, surfaces = read_with_surfaces(
        CommitmentFile("x", frozenset({"code"})),
        commitments=registry,
        as_of="2026-10-20",
    )
    assert reading.status.value == "OUTSIDE_SCOPE"
    assert not reading.registry_digest
    assert not surfaces
    assert reading.intake_notes


def test_small_valid_registry_is_usable():
    reading, surfaces = read_with_surfaces(
        CommitmentFile("x", frozenset({"code"})),
        commitments=BLUE_COMMITMENTS[:1],
        as_of="2026-10-20",
    )
    assert reading.findings
    assert surfaces


def test_iterator_is_explicitly_rejected_without_consumption():
    labels = iter(["handover_note", "run_instructions"])
    reading, surfaces = read_with_surfaces(
        CommitmentFile("x", frozenset({"code"}), labels), as_of="2026-10-20"
    )
    assert reading.intake_notes
    assert list(labels) == ["handover_note", "run_instructions"]
    assert all(not s.present for s in surfaces)


def test_findings_and_surfaces_agree():
    signals = ["handover_note"]
    reading, surfaces = read_with_surfaces(
        CommitmentFile("x", frozenset({"code"}), signals), as_of="2026-10-20"
    )
    for finding, surface in zip(reading.findings, surfaces):
        assert finding.commitment_id == surface.commitment_id
        assert (finding.status.value == "MAINTAINED") == (not surface.missing)
        assert (finding.status.value == "STALE") == bool(surface.stale)
        assert set(surface.stale) <= set(surface.missing)


@pytest.mark.parametrize("registry", [None, 3, iter(())])
def test_registry_checker_fails_closed_on_nonsized_input(registry):
    checks = invariants_hold(registry)
    assert any(not ok for _, ok, _ in checks)
    reading, surfaces = read_with_surfaces(
        CommitmentFile("x", frozenset({"code"})),
        commitments=registry,
        as_of="2026-10-20",
    )
    assert reading.status.value == "OUTSIDE_SCOPE"
    assert not surfaces
