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
    assert "--as-of requires" in result.stderr


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
