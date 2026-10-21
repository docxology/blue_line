import json
from copy import deepcopy
from dataclasses import replace

import pytest

from blue_line.evaluator import read_with_surfaces
from blue_line.records import CommitmentFile
from blue_line.report import ReportReplayError, build_report, replay_report, stewardship_worklist
from blue_line.serialization import context_digest, reading_digest, replay_digest


def test_report_roundtrip_replays_normalized_input():
    file = CommitmentFile(" source ", frozenset({"code", "unknown"}), frozenset({" handover_note "}),
                          declared_owner="Daniel", declared_next_review="2026-11-01", source_reference="git:revision")
    reading, surfaces = read_with_surfaces(file, as_of="2026-10-20", max_signal_age_days=30)
    report = json.loads(json.dumps(build_report(reading, surfaces)))
    assert replay_report(report) == (reading, surfaces)


def test_projection_equality_does_not_imply_input_or_policy_identity():
    file = CommitmentFile("one", frozenset({"code"}))
    a, _ = read_with_surfaces(file, as_of="2026-10-20", max_signal_age_days=30)
    b, _ = read_with_surfaces(replace(file, description="two"), as_of="2026-10-20", max_signal_age_days=180)
    assert reading_digest(a) == reading_digest(b)
    assert a.context.input_digest != b.context.input_digest
    assert context_digest(a.context) != context_digest(b.context)
    assert replay_digest(a) != replay_digest(b)
    changed = replace(a.context, evaluator_version="other")
    assert context_digest(changed) != context_digest(a.context)
    assert replay_digest(replace(a, registry_version="other")) != replay_digest(a)


@pytest.mark.parametrize("field", ["schema_version", "input", "context", "context_digest", "projection", "replay_digest", "registry_version", "surfaces"])
def test_replay_rejects_mutated_records(field):
    reading, surfaces = read_with_surfaces(CommitmentFile("one", frozenset({"code"})), as_of="2026-10-20")
    payload = deepcopy(build_report(reading, surfaces))
    payload[field] = None
    with pytest.raises(ReportReplayError):
        replay_report(payload)


def test_worklist_uses_same_surfaces_without_inventing_dates():
    reading, surfaces = read_with_surfaces(CommitmentFile("one", frozenset({"code"})), as_of="2026-10-20")
    rows = stewardship_worklist(reading, surfaces)
    assert {(r["commitment_id"], r["signal"]) for r in rows} == {
        (s.commitment_id, signal) for s in surfaces for signal in s.missing}
    assert all(r["declared_next_review"] is None and r["declared_owner"] is None for r in rows)


def test_worklist_retains_declared_metadata():
    reading, surfaces = read_with_surfaces(CommitmentFile("one", frozenset({"code"}),
        declared_owner="owner", declared_next_review="2026-11-01", source_reference="ref"), as_of="2026-10-20")
    assert all(r["declared_owner"] == "owner" and r["declared_next_review"] == "2026-11-01"
               and r["source_reference"] == "ref" for r in stewardship_worklist(reading, surfaces))


def test_subject_identity_is_separate_from_report_content():
    from blue_line.envelope import build_envelope, envelope_digest
    reading, _ = read_with_surfaces(CommitmentFile("one", frozenset({"code"})), as_of="2026-10-20")
    a = build_envelope(reading, subject_id="a")
    b = build_envelope(reading, subject_id="b")
    assert a["report_ref"] == b["report_ref"]
    assert envelope_digest(a) != envelope_digest(b)


def test_prepared_reports_replay_and_bind_envelopes():
    from pathlib import Path
    from blue_line.envelope import envelope_digest
    root = Path(__file__).resolve().parents[1] / "data"
    for path in sorted((root / "reports").glob("*.json")):
        report = json.loads(path.read_text())
        replay_report(report)
        binding = json.loads((root / "report_bindings" / path.name).read_text())
        envelope = json.loads((root / "envelopes" / path.name).read_text())
        assert binding["replay_digest"] == report["replay_digest"]
        assert binding["envelope_digest"] == envelope_digest(envelope)
        assert envelope["report_ref"] == report["projection_digest"]
    assert list((root / "reports").glob("*.json"))


@pytest.mark.parametrize("spelling", ["20261020", "2026-W43-2", "2026-10-20"])
def test_accepted_library_dates_roundtrip(spelling):
    from blue_line.records import CareSignal
    reading, surfaces = read_with_surfaces(CommitmentFile("ISO date", frozenset({"code"}),
        dated_evidence=(CareSignal("handover_note", spelling),)), as_of="2026-10-20")
    assert not reading.intake_notes
    assert replay_report(json.loads(json.dumps(build_report(reading, surfaces)))) == (reading, surfaces)
    assert reading.normalized_input.dated_evidence[0].noted_on == "2026-10-20"
