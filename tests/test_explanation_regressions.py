from blue_line.evaluator import read_with_surfaces
from blue_line.records import CareSignal, CommitmentFile
from blue_line.registry import BLUE_COMMITMENTS
from blue_line.serialization import registry_digest

import pytest


@pytest.mark.parametrize("renewal", [None, "2026-10-20"])
def test_renewal_overrides_raw_staleness(renewal):
    reading, surfaces = read_with_surfaces(
        CommitmentFile(
            "renewed",
            frozenset({"code"}),
            dated_evidence=(
                CareSignal("handover_note", "2025-01-01"),
                CareSignal("handover_note", renewal),
            ),
        ),
        as_of="2026-10-20",
    )
    assert reading.findings
    for surface in surfaces:
        assert set(surface.stale) <= set(surface.missing)
        assert "handover_note" not in surface.missing
        assert "handover_note" not in surface.stale


def test_future_date_has_review_diagnostic_separate_from_intake():
    reading, surfaces = read_with_surfaces(
        CommitmentFile(
            "future",
            frozenset({"code"}),
            dated_evidence=(CareSignal("handover_note", "2027-01-01"),),
        ),
        as_of="2026-10-20",
    )
    assert not reading.intake_notes
    assert reading.review_notes
    assert all("handover_note" not in s.present for s in surfaces)


def test_invalid_date_is_intake_diagnostic():
    reading, _ = read_with_surfaces(
        CommitmentFile(
            "invalid",
            frozenset({"code"}),
            dated_evidence=(CareSignal("handover_note", "bad"),),
        ),
        as_of="2026-10-20",
    )
    assert reading.intake_notes


def test_registry_digest_binds_declaration_order():
    assert registry_digest(tuple(reversed(BLUE_COMMITMENTS))) != registry_digest(
        BLUE_COMMITMENTS
    )
