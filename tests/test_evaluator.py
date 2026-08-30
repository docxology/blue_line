"""The verdict function: fresh, partial, stale, fail-closed, and intake paths."""

from __future__ import annotations

from datetime import date

import pytest

from blue_line.enums import FileStatus, StewardshipStatus
from blue_line.evaluator import read_file, read_with_surfaces
from blue_line.records import CareSignal, CommitmentFile
from blue_line.registry import BLUE_COMMITMENTS


def test_full_declaration_reads_maintained(maintained_file, review_date):
    reading = read_file(maintained_file, as_of=review_date)
    assert reading.status is FileStatus.MAINTAINED
    assert all(f.status is StewardshipStatus.MAINTAINED for f in reading.findings)


def test_partial_declaration_reads_needs_attention(review_date):
    reading = read_file(
        CommitmentFile(
            description="a repo with a handover note and continuity notes",
            tags=frozenset({"code", "docs"}),
            evidence=frozenset({"handover_note", "continuity_note"}),
        ),
        as_of=review_date,
    )
    assert reading.status is FileStatus.NEEDS_ATTENTION
    assert any(f.status is StewardshipStatus.NEEDS_ATTENTION for f in reading.findings)
    assert any(f.status is StewardshipStatus.MAINTAINED for f in reading.findings)


def test_aged_signals_read_stale(stale_file, review_date):
    reading = read_file(stale_file, as_of=review_date)
    assert reading.status is FileStatus.STALE
    assert any(f.status is StewardshipStatus.STALE for f in reading.findings)


def test_empty_scan_set_fails_closed(review_date):
    reading = read_file(
        CommitmentFile(description="nothing declared"), as_of=review_date
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert reading.findings == ()
    assert any("nothing was read" in note for note in reading.intake_notes)


def test_blank_description_blocks(review_date):
    reading = read_file(CommitmentFile(description="   "), as_of=review_date)
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert reading.findings == ()


def test_non_record_input_is_set_aside(review_date):
    reading = read_file("not a file", as_of=review_date)  # type: ignore[arg-type]
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("not a CommitmentFile" in note for note in reading.intake_notes)


def test_unknown_tags_set_aside_not_crash(review_date):
    reading = read_file(
        CommitmentFile(
            description="odd tags",
            tags=frozenset({"code", "quantum"}),
            evidence=frozenset(CODE_DOCS_ALL),
        ),
        as_of=review_date,
    )
    assert reading.status is FileStatus.MAINTAINED
    assert any("unknown tag" in note for note in reading.intake_notes)


CODE_DOCS_ALL = {
    "handover_note",
    "run_instructions",
    "status_note",
    "check_run",
    "check_result",
    "dependency_review",
    "downstream_list",
    "triage_log",
    "continuity_note",
    "review_note",
    "rerun_result",
    "cadence_statement",
    "retirement_note",
    "obligation_entry",
}


def test_unknown_tags_block_when_strict(review_date):
    reading = read_file(
        CommitmentFile(
            description="odd tags",
            tags=frozenset({"code", "quantum"}),
            evidence=frozenset(CODE_DOCS_ALL),
        ),
        as_of=review_date,
        allow_unknown_tags=False,
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("unknown tags block" in note for note in reading.intake_notes)


def test_malformed_labels_become_notes(review_date):
    reading = read_file(
        CommitmentFile(
            description="sloppy declarations",
            tags=frozenset({"code", 42}),  # type: ignore[set-item]
            evidence=frozenset({"", 7}),  # type: ignore[set-item]
        ),
        as_of=review_date,
    )
    assert reading.status is FileStatus.NEEDS_ATTENTION
    assert any("malformed" in note for note in reading.intake_notes)


def test_malformed_dated_record_is_set_aside(review_date):
    class Bad:
        label = ""
        noted_on = "2026-01-01"

    class Undatable:
        label = "handover_note"
        noted_on = "not-a-date"

    reading = read_file(
        CommitmentFile(
            description="broken dated records",
            tags=frozenset({"code"}),
            dated_evidence=(Bad(), Undatable()),
        ),
        as_of=review_date,
    )
    assert any("unreadable" in note or "without a usable label" in note for note in reading.intake_notes)


def test_future_dated_signal_not_fresh(review_date):
    reading = read_file(
        CommitmentFile(
            description="claims care from the future",
            tags=frozenset({"code", "docs"}),
            dated_evidence=(
                CareSignal(label="handover_note", noted_on="2027-01-01"),
            ),
            evidence=frozenset(CODE_DOCS_ALL - {"handover_note"}),
        ),
        as_of=review_date,
    )
    assert reading.status is not FileStatus.MAINTAINED


def test_undated_dated_evidence_counts_fresh(review_date):
    reading = read_file(
        CommitmentFile(
            description="undated declarations",
            tags=frozenset({"code", "docs"}),
            dated_evidence=(CareSignal(label="handover_note"),),
            evidence=frozenset(CODE_DOCS_ALL - {"handover_note"}),
        ),
        as_of=review_date,
    )
    assert reading.status is FileStatus.MAINTAINED


def test_bad_as_of_string_raises(review_date):
    with pytest.raises(ValueError):
        read_file(
            CommitmentFile(description="x", tags=frozenset({"code"})),
            as_of="not-a-date",
        )


def test_bad_as_of_type_raises(review_date):
    with pytest.raises(TypeError):
        read_file(
            CommitmentFile(description="x", tags=frozenset({"code"})),
            as_of=3.5,  # type: ignore[arg-type]
        )


def test_negative_max_age_raises(review_date):
    with pytest.raises(ValueError):
        read_file(
            CommitmentFile(description="x", tags=frozenset({"code"})),
            as_of=review_date,
            max_signal_age_days=-1,
        )


def test_bad_max_age_type_raises(review_date):
    with pytest.raises(TypeError):
        read_file(
            CommitmentFile(description="x", tags=frozenset({"code"})),
            as_of=review_date,
            max_signal_age_days="30",  # type: ignore[arg-type]
        )


def test_bool_max_age_rejected(review_date):
    with pytest.raises(TypeError):
        read_file(
            CommitmentFile(description="x", tags=frozenset({"code"})),
            as_of=review_date,
            max_signal_age_days=True,
        )


def test_zero_window_counts_recent_as_stale(review_date):
    reading = read_file(
        CommitmentFile(
            description="yesterday is already old here",
            tags=frozenset({"code", "docs"}),
            dated_evidence=(
                CareSignal(label="handover_note", noted_on="2026-07-31"),
            ),
            evidence=frozenset(CODE_DOCS_ALL - {"handover_note"}),
        ),
        as_of=review_date,
        max_signal_age_days=0,
    )
    assert reading.status is not FileStatus.MAINTAINED


def test_reading_pins_registry_digest(maintained_file, review_date):
    from blue_line.serialization import registry_digest

    reading = read_file(maintained_file, as_of=review_date)
    assert reading.registry_digest == registry_digest()


def test_broken_custom_registry_fails_closed(review_date):
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        commitments=(BLUE_COMMITMENTS[0], BLUE_COMMITMENTS[0]),
        as_of=review_date,
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("duplicate id" in note for note in reading.intake_notes)


def test_non_commitment_registry_entry_fails_closed(review_date):
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        commitments=("nope",),  # type: ignore[arg-type]
        as_of=review_date,
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("not a Commitment record" in note for note in reading.intake_notes)


def test_blank_registry_field_fails_closed(review_date):
    from blue_line.records import Commitment

    broken = Commitment(" ", "t", "w", frozenset({"code"}), ("s",))
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        commitments=(broken,),
        as_of=review_date,
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("blank or non-text" in note for note in reading.intake_notes)


def test_malformed_registry_tags_fail_closed(review_date):
    from blue_line.records import Commitment

    broken = Commitment("ok", "t", "w", frozenset(), ("s",))
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        commitments=(broken,),
        as_of=review_date,
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("malformed tags" in note for note in reading.intake_notes)


def test_malformed_registry_signals_fail_closed(review_date):
    from blue_line.records import Commitment

    broken = Commitment("ok", "t", "w", frozenset({"code"}), ())
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        commitments=(broken,),
        as_of=review_date,
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("malformed required signals" in note for note in reading.intake_notes)


def test_bad_registry_kind_fails_closed(review_date):
    from blue_line.records import Commitment

    broken = Commitment("ok", "t", "w", frozenset({"code"}), ("s",), kind="SYSTEM")  # type: ignore[arg-type]
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        commitments=(broken,),
        as_of=review_date,
    )
    assert reading.status is FileStatus.OUTSIDE_SCOPE
    assert any("invalid kind" in note for note in reading.intake_notes)


def test_date_object_as_of_accepted(review_date):
    reading = read_file(
        CommitmentFile(description="x", tags=frozenset({"code"})),
        as_of=date.fromisoformat(review_date),
    )
    assert reading.read_as_of == review_date


def test_surfaces_match_findings(stale_file, review_date):
    reading, surfaces = read_with_surfaces(stale_file, as_of=review_date)
    assert reading.findings
    assert len(surfaces) == len(reading.findings)
    for surface in surfaces:
        assert set(surface.stale) <= set(surface.missing)
        assert surface.present or surface.missing


def test_surfaces_empty_for_blocked_intake(review_date):
    reading, surfaces = read_with_surfaces(
        CommitmentFile(description="  "), as_of=review_date
    )
    assert surfaces == ()
    assert reading.status is FileStatus.OUTSIDE_SCOPE


def test_default_as_of_uses_today():
    reading = read_file(CommitmentFile(description="x", tags=frozenset({"code"})))
    assert reading.read_as_of == date.today().isoformat()
