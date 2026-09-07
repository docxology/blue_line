"""The read-file command body in blue_line.cli, exercised directly."""

from __future__ import annotations

import json

from blue_line.cli import read_file_main

STALE_PAYLOAD = json.dumps(
    {
        "description": "an aging repo",
        "tags": ["code"],
        "dated_evidence": [{"label": "check_run", "noted_on": "2025-06-01"}],
    }
)


def test_read_file_main_rejects_bad_json(capsys):
    assert read_file_main(["{not json"]) == 2
    assert "invalid JSON" in capsys.readouterr().err


def test_read_file_main_rejects_missing_as_of_value(capsys):
    assert read_file_main(['{"description": "x"}', "--as-of"]) == 2
    assert "--as-of requires" in capsys.readouterr().err


def test_read_file_main_rejects_wrong_arity(capsys):
    assert read_file_main([]) == 2
    assert "usage: read_file_cli.py" in capsys.readouterr().err


def test_read_file_main_prints_reading_json(capsys):
    code = read_file_main([STALE_PAYLOAD, "--as-of", "2026-08-01"])
    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data["status"] == "STALE"
    assert isinstance(data["findings"], list)
    assert isinstance(data["surfaces"], list)
