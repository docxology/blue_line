"""Envelope construction and the prepared witness envelopes in data/."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from dataclasses import replace

import blue_line
from blue_line.records import CommitmentFile
from blue_line.evaluator import read_file

REPO = Path(__file__).resolve().parents[1]
ENVDIR = REPO / "data" / "envelopes"
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


@pytest.mark.parametrize("case", ["subject", "blocked", "registry", "date", "digest", "version", "refs"])
def test_builder_enforces_eligibility_and_identity(case):
    reading = read_file(_worked_file(), as_of="2026-08-01")
    subject = "subject"
    refs = ()
    if case == "subject":
        subject = " "
    elif case == "blocked":
        reading = read_file(CommitmentFile(""), as_of="2026-08-01")
    elif case == "registry":
        reading = read_file(_worked_file(), commitments=("bad",), as_of="2026-08-01")
    elif case == "date":
        reading = replace(reading, read_as_of="")
    elif case == "digest":
        reading = replace(reading, registry_digest="")
    elif case == "version":
        reading = replace(reading, registry_version="")
    else:
        refs = (" ",)
    with pytest.raises(ValueError):
        blue_line.build_envelope(reading, subject_id=subject, source_snapshot_refs=refs)


@pytest.mark.parametrize("changes", [{"max_signal_age_days": -1}, {"max_signal_age_days": True},
    {"max_signal_age_days": None}, {"allow_unknown_tags": None}, {"allow_unknown_tags": 1}])
def test_builder_and_helper_reject_invalid_context_policy(changes):
    reading = read_file(_worked_file(), as_of="2026-08-01")
    reading = replace(reading, context=replace(reading.context, **changes))
    assert not blue_line.envelope_matches_reading(reading)
    with pytest.raises(blue_line.EnvelopeEligibilityError):
        blue_line.build_envelope(reading, subject_id="subject")


@pytest.mark.parametrize("field", ["subject_id", "source_snapshot_refs"])
@pytest.mark.parametrize(
    "text",
    ["\ud800", "\udbff", "\udc00", "\udfff", "prefix\ud955suffix", "\ud83d\udcd8"],
)
def test_public_builder_rejects_non_scalar_transport_identity(field, text):
    reading = blue_line.read_file(_worked_file(), as_of="2026-08-01")
    metadata = {"subject_id": "subject", "source_snapshot_refs": ("snapshot",)}
    metadata[field] = text if field == "subject_id" else ("snapshot", text)
    with pytest.raises(blue_line.EnvelopeEligibilityError) as caught:
        blue_line.build_envelope(reading, **metadata)
    assert caught.value.field == field


def test_public_builder_preserves_scalar_metadata_and_canonical_reference_order():
    reading = blue_line.read_file(_worked_file(), as_of="2026-08-01")
    subject = "sujet-é-📘"
    refs = ("z-資料-🧭", "a-e\u0301-📘", "a-é-📘", "z-資料-🧭")
    envelope = blue_line.build_envelope(
        reading, subject_id=subject, source_snapshot_refs=refs
    )
    expected = blue_line.build_envelope(reading, subject_id="subject")
    expected["subject_id"] = subject
    expected["source_snapshot_refs"] = ["a-e\u0301-📘", "a-é-📘", "z-資料-🧭"]
    assert envelope == expected
    canonical_bytes = json.dumps(expected, sort_keys=True).encode("utf-8")
    assert (
        blue_line.envelope_digest(envelope)
        == hashlib.sha256(canonical_bytes).hexdigest()
    )


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


