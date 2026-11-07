import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from blue_line.examples import write_examples
from blue_line.publication import check_publication_main
from blue_line.report import ReportReplayError, build_report, replay_report
from blue_line.evaluator import read_file
from blue_line.records import CommitmentFile
from blue_line.version import __version__

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("mutation", ["none", "version", "doi"])
def test_publication_gate_with_real_negative_controls(tmp_path, mutation, capsys):
    for name in (
        "pyproject.toml",
        "CITATION.cff",
        ".zenodo.json",
        "docs/manuscript/config.yaml",
        "docs/manuscript/references.bib",
    ):
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    cff = tmp_path / "CITATION.cff"
    if mutation == "version":
        cff.write_text(
            cff.read_text().replace(f"version: {__version__}", "version: 999.0.0")
        )
    elif mutation == "doi":
        cff.write_text(cff.read_text().replace("10.5281/zenodo.", "10.9999/zenodo."))
    assert check_publication_main(tmp_path) == (0 if mutation == "none" else 1)
    assert ("FAIL" in capsys.readouterr().out) == (mutation != "none")


def test_example_regeneration_is_idempotent_on_real_files(tmp_path):
    shutil.copytree(ROOT / "data/declared_files", tmp_path / "data/declared_files")
    shutil.copyfile(ROOT / "data/example_contexts.json", tmp_path / "data/example_contexts.json")
    first = {p.relative_to(tmp_path): p.read_bytes() for p in write_examples(tmp_path)}
    for path in first:
        (tmp_path / path).write_text("corrupted generated output")
    second = {p.relative_to(tmp_path): p.read_bytes() for p in write_examples(tmp_path)}
    assert first == second
    for path in sorted((tmp_path / "data/reports").glob("*.json")):
        replay_report(json.loads(path.read_text()))


def test_new_scripts_work_as_subprocesses(tmp_path):
    for name in ("src", "scripts", "data", "docs/manuscript"):
        shutil.copytree(ROOT / name, tmp_path / name)
    for name in ("pyproject.toml", "CITATION.cff", ".zenodo.json"):
        shutil.copyfile(ROOT / name, tmp_path / name)
    result = subprocess.run(
        [sys.executable, str(tmp_path / "scripts/gen_examples.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    for path in sorted((tmp_path / "data/reports").glob("*.json")):
        report = json.loads(path.read_text())
        replay_report(report)
        binding = json.loads(
            (tmp_path / "data/report_bindings" / path.name).read_text()
        )
        assert binding["replay_digest"] == report["replay_digest"]
        assert binding["projection_digest"] == report["projection_digest"]
    publication_script = tmp_path / "scripts/check_publication.py"
    accepted = subprocess.run(
        [sys.executable, str(publication_script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert accepted.returncode == 0, accepted.stderr
    cff = tmp_path / "CITATION.cff"
    cff.write_text(
        cff.read_text().replace(f"version: {__version__}", "version: 999.0.0")
    )
    rejected = subprocess.run(
        [sys.executable, str(publication_script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert rejected.returncode == 1


@pytest.mark.parametrize(
    "metadata",
    [
        {"declared_owner": 4},
        {"source_reference": ""},
        {"declared_next_review": "invalid"},
        {"declared_next_review": "20261021"},
    ],
)
def test_invalid_json_metadata_is_a_usage_error(metadata, capsys):
    from blue_line.cli import read_file_main

    assert read_file_main([json.dumps({"description": "x", **metadata})]) == 2
    assert capsys.readouterr().err


def test_library_bad_metadata_is_set_aside():
    reading = read_file(
        CommitmentFile(
            "x",
            frozenset({"code"}),
            declared_owner=4,
            source_reference="",
            declared_next_review="invalid",
        ),
        as_of="2026-10-20",
    )
    assert reading.normalized_input.declared_owner is None
    assert reading.normalized_input.source_reference is None
    assert reading.normalized_input.declared_next_review is None
    assert len(reading.intake_notes) == 3


def test_blocked_reading_cannot_be_exported_as_replayable_report():
    with pytest.raises(ReportReplayError):
        build_report(read_file(CommitmentFile(""), as_of="2026-10-20"), ())


def test_replay_rejects_bad_date_without_traceback():
    from blue_line.evaluator import read_with_surfaces

    reading, surfaces = read_with_surfaces(
        CommitmentFile("x", frozenset({"code"})), as_of="2026-10-20"
    )
    payload = build_report(reading, surfaces)
    payload["context"]["read_as_of"] = "bad"
    with pytest.raises(ReportReplayError):
        replay_report(payload)
