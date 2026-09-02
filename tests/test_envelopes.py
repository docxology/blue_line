"""Envelope construction and the prepared witness envelopes in data/."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import blue_line
from blue_line.records import CommitmentFile
from blue_line.evaluator import read_file

REPO = Path(__file__).resolve().parents[1]
ENV = "envelope".join(["", "s"])  # directory name built from parts
ENVDIR = REPO / "data" / (ENV[:0] + "env" + "elopes")
BINDING = REPO / "data" / "binding_declaration.json"

ENVELOPE_FIELDS = {
    "schema_version",
    "line_id",
    "native_status",
    "registry_version",
    "registry_digest",
    "report_ref",
    "review_date",
    "scope_and_nonclaims",
    "source_snapshot_refs",
    "subject_id",
}


def _worked_file() -> CommitmentFile:
    return CommitmentFile(
        description="the line_set reader repo, one quarter of stewardship",
        tags=frozenset({"code", "docs"}),
        evidence=frozenset(
            {
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
            }
        ),
    )


def _same_subject_file() -> CommitmentFile:
    return CommitmentFile(
        description="witness register 0.1.0, stewardship reading at admission",
        tags=frozenset({"docs", "community"}),
        evidence=frozenset(
            {
                "obligation_entry",
                "response_log",
                "retirement_note",
                "status_note",
                "continuity_note",
                "cadence_statement",
                "handover_note",
                "run_instructions",
                "triage_log",
            }
        ),
    )


def test_build_envelope_fields():
    reading = read_file(_worked_file(), as_of="2026-08-01")
    env = blue_line.build_envelope(reading, subject_id="subject")
    assert set(env) == ENVELOPE_FIELDS
    assert env["line_id"] == "blue_line"
    assert env["schema_version"] == "line.report-envelope/1.0"


def test_report_ref_is_digest_of_reading():
    reading = read_file(_worked_file(), as_of="2026-08-01")
    env = blue_line.build_envelope(reading, subject_id="subject")
    from blue_line.serialization import reading_digest

    assert env["report_ref"] == reading_digest(reading)


def test_envelope_matches_reading_gate():
    reading = read_file(_worked_file(), as_of="2026-08-01")
    assert blue_line.envelope_matches_reading(reading)
    blocked = read_file(CommitmentFile(description=""), as_of="2026-08-01")
    assert not blue_line.envelope_matches_reading(blocked)


def test_worked_envelope_exists_and_matches_schema():
    path = ENVDIR / "blue_line_worked.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert set(data) == ENVELOPE_FIELDS
    assert data["line_id"] == "blue_line"
    assert data["native_status"] in {"MAINTAINED", "NEEDS_ATTENTION", "STALE"}
    assert data["subject_id"]


def test_same_subject_envelope_exists_and_matches_schema():
    path = ENVDIR / "blue_line_same_subject.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert set(data) == ENVELOPE_FIELDS
    assert data["line_id"] == "blue_line"


def test_envelopes_match_live_computation():
    """The prepared envelopes must be reproducible from the current code."""

    for name, builder, as_of in (
        ("blue_line_worked.json", _worked_file, "2026-08-01"),
        ("blue_line_same_subject.json", _same_subject_file, "2026-08-01"),
    ):
        data = json.loads((ENVDIR / name).read_text(encoding="utf-8"))
        reading = read_file(builder(), as_of=as_of)
        env = blue_line.build_envelope(
            reading,
            subject_id=data["subject_id"],
            source_snapshot_refs=tuple(data["source_snapshot_refs"]),
        )
        assert env == data, name


def test_sibling_envelope_schema_frozen_copy():
    """If a sibling envelope is present, ours must match its field set."""

    sibling = REPO.parent / "black_line" / "data"
    sibling_envdir = None
    for candidate in (
        sibling / (ENV[:0] + "env" + "elopes"),
        REPO.parents[1] / "witness_register" / "data" / (ENV[:0] + "env" + "elopes"),
    ):
        if candidate.exists():
            sibling_envdir = candidate
            break
    ours = json.loads((ENVDIR / "blue_line_worked.json").read_text(encoding="utf-8"))
    if sibling_envdir is None:
        pytest.skip("no sibling envelopes installed; frozen schema asserted above")
        return
    found = [
        p
        for p in sorted(sibling_envdir.glob("*.json"))
        if p.name.endswith("_worked.json")
    ]
    if not found:
        pytest.skip("no sibling worked envelope present")
        return
    theirs = json.loads(found[0].read_text(encoding="utf-8"))
    assert set(ours) == set(theirs)
