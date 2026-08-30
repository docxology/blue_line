"""Thin CLIs run as subprocesses against real data."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

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
    assert "FAIL" not in result.stdout


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


def test_read_file_cli_bad_json():
    result = _run("read_file_cli.py", "{not json")
    assert result.returncode == 2


def test_read_file_cli_no_args():
    result = _run("read_file_cli.py")
    assert result.returncode == 2


def test_build_figures_script(tmp_path: Path):
    result = _run("build_figures.py")
    assert result.returncode == 0, result.stderr
    out = REPO / "output" / "figures"
    assert (out / "figure_registry.json").exists()


def test_gen_ledger_script():
    result = _run("gen_formalism_ledger.py")
    assert result.returncode == 0, result.stderr
    assert (REPO / "data" / "formalism_claim_ledger.json").exists()
