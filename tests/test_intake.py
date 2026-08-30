"""Intake staging: set-asides with notes, never exceptions or invented values."""

from __future__ import annotations

from blue_line.enums import FileStatus
from blue_line.intake import intake
from blue_line.records import CareSignal, CommitmentFile


def test_non_record_input_rejected():
    file, status, notes = intake("garbage")
    assert file is None
    assert status is FileStatus.OUTSIDE_SCOPE
    assert notes


def test_blank_description_blocks():
    file, status, notes = intake(CommitmentFile(description=""))
    assert file is None
    assert status is FileStatus.OUTSIDE_SCOPE
    assert any("blank" in note for note in notes)


def test_malformed_tag_set_aside():
    file, _status, notes = intake(
        CommitmentFile(description="ok", tags=frozenset({"code", 3}))  # type: ignore[set-item]
    )
    assert file is not None
    assert file.tags == frozenset({"code"})
    assert any("malformed tag" in note for note in notes)


def test_string_tags_rejected_whole():
    file, _status, notes = intake(
        CommitmentFile(description="ok", tags="code")  # type: ignore[arg-type]
    )
    assert file is not None
    assert file.tags == frozenset()
    assert any("not a collection" in note for note in notes)


def test_blank_signal_label_set_aside():
    file, _status, notes = intake(
        CommitmentFile(description="ok", dated_evidence=(CareSignal(label="  "),))
    )
    assert file is not None
    assert file.dated_evidence == ()
    assert any("without a usable label" in note for note in notes)


def test_undatable_signal_set_aside():
    file, _status, notes = intake(
        CommitmentFile(
            description="ok",
            dated_evidence=(CareSignal(label="check_run", noted_on="yesterday"),),
        )
    )
    assert file is not None
    assert file.dated_evidence == ()
    assert any("unreadable" in note for note in notes)


def test_non_string_date_set_aside():
    file, _status, notes = intake(
        CommitmentFile(
            description="ok",
            dated_evidence=(CareSignal(label="check_run", noted_on=20260801),),  # type: ignore[arg-type]
        )
    )
    assert file is not None
    assert file.dated_evidence == ()
    assert any("non-string date" in note for note in notes)


def test_good_signals_pass_through():
    file, _status, _notes = intake(
        CommitmentFile(
            description="ok",
            dated_evidence=(CareSignal(label="Check_Run", noted_on="2026-08-01"),),
        )
    )
    assert file is not None
    assert file.dated_evidence == (CareSignal(label="check_run", noted_on="2026-08-01"),)


def test_description_stripped():
    file, _status, _notes = intake(CommitmentFile(description="  padded  "))
    assert file is not None
    assert file.description == "padded"


def test_unknown_tag_note_and_strict_block():
    file, _status, notes = intake(
        CommitmentFile(description="ok", tags=frozenset({"code", "zeta"}))
    )
    assert file is not None
    assert any("unknown tag" in note for note in notes)
    file2, status2, notes2 = intake(
        CommitmentFile(description="ok", tags=frozenset({"code", "zeta"})),
        allow_unknown_tags=False,
    )
    assert file2 is None
    assert status2 is FileStatus.OUTSIDE_SCOPE
    assert any("unknown tags block" in note for note in notes2)
