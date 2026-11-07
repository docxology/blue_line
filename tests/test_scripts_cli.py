"""Thin CLIs run as subprocesses against real data."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


from blue_line.figures import FIGURE_SPECS
from blue_line.ledger import build_formalism_ledger
from blue_line.serialization import registry_digest

REPO = Path(__file__).resolve().parents[1]
PY = sys.executable


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(REPO / "scripts" / script), *args],
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_check_registry_cli_passes():
    result = _run("check_registry.py")
    assert result.returncode == 0, result.stdout + result.stderr


def test_read_file_cli_maintained():
    payload = json.dumps(
        {
            "description": "a well-tended repo",
            "tags": ["code", "docs"],
            "evidence": [
                "cadence_statement",
                "check_result",
                "check_run",
                "continuity_note",
                "dependency_review",
                "downstream_list",
                "handover_note",
                "obligation_entry",
                "rerun_result",
                "retirement_note",
                "review_note",
                "run_instructions",
                "status_note",
                "triage_log",
            ],
        }
    )
    result = _run("read_file_cli.py", payload)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["status"] == "MAINTAINED"


def test_read_file_cli_as_of_override():
    payload = json.dumps(
        {
            "description": "an aging repo",
            "tags": ["code"],
            "dated_evidence": [{"label": "check_run", "noted_on": "2025-06-01"}],
        }
    )
    fresh = _run("read_file_cli.py", payload, "--as-of", "2025-07-01")
    stale = _run("read_file_cli.py", payload, "--as-of", "2026-08-01")
    assert fresh.returncode == 0 and stale.returncode == 0
    # tag "code" matches commitments that need more signals than check_run,
    # so the fresh case is NEEDS_ATTENTION while the stale case flips to STALE.
    assert json.loads(fresh.stdout)["status"] == "NEEDS_ATTENTION"
    assert json.loads(stale.stdout)["status"] == "STALE"


def test_read_file_cli_as_of_missing_value():
    result = _run("read_file_cli.py", '{"description": "x"}', "--as-of")
    assert result.returncode == 2
    assert result.stderr
    assert not result.stdout


def test_read_file_cli_bad_json():
    result = _run("read_file_cli.py", "{not json")
    assert result.returncode == 2


def test_read_file_cli_no_args():
    result = _run("read_file_cli.py")
    assert result.returncode == 2


def _sandbox(tmp_path: Path) -> Path:
    sandbox = tmp_path / "blue_line"
    shutil.copytree(REPO / "src", sandbox / "src")
    shutil.copytree(REPO / "scripts", sandbox / "scripts")
    return sandbox


def test_build_figures_script(tmp_path: Path):
    sandbox = _sandbox(tmp_path)
    result = subprocess.run(
        [PY, str(sandbox / "scripts" / "build_figures.py")],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    out = sandbox / "output" / "figures"
    manifest = json.loads((out / "figure_registry.json").read_text())
    assert manifest["registry_digest"] == registry_digest()
    assert {entry["figure_id"] for entry in manifest["figures"]} == {
        spec.figure_id for spec in FIGURE_SPECS
    }
    for entry in manifest["figures"]:
        image = out / entry["filename"]
        assert image.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        assert image.stat().st_size == entry["bytes"]


def test_gen_ledger_script(tmp_path: Path):
    sandbox = _sandbox(tmp_path)
    result = subprocess.run(
        [PY, str(sandbox / "scripts" / "gen_formalism_ledger.py")],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(
        (sandbox / "data" / "formalism_claim_ledger.json").read_text()
    ) == (build_formalism_ledger())
