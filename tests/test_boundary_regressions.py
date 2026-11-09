"""Executed counterexamples for the date and JSON review findings."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

from blue_line.cli import read_file_main
from blue_line.evaluator import read_file
from blue_line.records import CareSignal, CommitmentFile
from blue_line.registry import BLUE_COMMITMENTS

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "read_file_cli.py"
CODE_SIGNALS = sorted(
    {s for c in BLUE_COMMITMENTS if "code" in c.tags for s in c.required_signals}
)


def dated_payload(noted_on: str) -> dict:
    return {
        "description": "review-date regression",
        "tags": ["code"],
        "dated_evidence": [{"label": s, "noted_on": noted_on} for s in CODE_SIGNALS],
    }


def test_cli_resolves_today_and_exposes_context(capsys):
    assert read_file_main([json.dumps(dated_payload("2026-03-01"))]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["read_as_of"] == date.today().isoformat()
    assert output["registry_version"]
    assert output["registry_digest"]


@pytest.mark.parametrize(
    ("review_date", "status"), [("2026-08-01", "MAINTAINED"), ("2026-10-20", "STALE")]
)
def test_historical_cli_dates_are_explicit(review_date, status):
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            json.dumps(dated_payload("2026-03-01")),
            "--as-of",
            review_date,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["status"] == status
    assert output["read_as_of"] == review_date


@pytest.mark.parametrize(("age", "status"), [(180, "MAINTAINED"), (181, "STALE")])
def test_freshness_window_is_inclusive(age, status):
    review_date = date(2026, 10, 20)
    file = CommitmentFile(
        "boundary",
        frozenset({"code"}),
        dated_evidence=tuple(
            CareSignal(s, (review_date - timedelta(days=age)).isoformat())
            for s in CODE_SIGNALS
        ),
    )
    assert read_file(file, as_of=review_date).status.value == status


BAD_PAYLOADS = [
    [],
    None,
    {"description": "x", "tags": None},
    {"description": "x", "tags": [{}]},
    {"description": "x", "tags": "code"},
    {"description": 4},
    {"description": "x", "dated_evidence": None},
    {"description": "x", "dated_evidence": "oops"},
    {"description": "x", "dated_evidence": [{}]},
    {"description": "x", "dated_evidence": [{"label": 1}]},
    {"description": "x", "dated_evidence": [{"label": "x", "noted_on": False}]},
    {"description": "x", "dated_evidence": [{"label": "x", "noted_on": "bad"}]},
    {"description": "x", "unknown_field": []},
]
BAD_PAYLOADS += [
    {
        "description": "x",
        "evidence": {
            s: value
            for s in (
                "obligation_entry",
                "response_log",
                "retirement_note",
                "cadence_statement",
            )
        },
        "tags": ["community"],
    }
    for value in (False, True)
]


@pytest.mark.parametrize("payload", BAD_PAYLOADS)
def test_malformed_shapes_return_usage_error_directly(payload, capsys):
    assert read_file_main([json.dumps(payload)]) == 2
    captured = capsys.readouterr()
    assert captured.err
    assert not captured.out


@pytest.mark.parametrize("payload", BAD_PAYLOADS)
def test_malformed_shapes_return_usage_error_in_subprocess(payload):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), json.dumps(payload)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert not result.stdout


@pytest.mark.parametrize("value", [False, True])
def test_library_mapping_cannot_declare_positive_evidence(value):
    file = CommitmentFile(
        "mapping",
        frozenset({"community"}),
        {
            s: value
            for s in (
                "obligation_entry",
                "response_log",
                "retirement_note",
                "cadence_statement",
            )
        },
    )
    reading = read_file(file, as_of="2026-10-20")
    assert reading.status.value == "NEEDS_ATTENTION"
    assert reading.intake_notes


@pytest.mark.parametrize(
    "review_date",
    [
        "20261020",
        "2026-W43-2",
        "invalid",
        "2026-02-29",
        "2026-13-01",
        "2026-10-20T00:00:00",
        " 2026-10-20",
    ],
)
def test_noncanonical_cli_date_is_usage_error_directly(review_date, capsys):
    assert (
        read_file_main(
            [json.dumps(dated_payload("2026-03-01")), "--as-of", review_date]
        )
        == 2
    )
    captured = capsys.readouterr()
    assert captured.err
    assert not captured.out


@pytest.mark.parametrize(
    "review_date",
    [
        "20261020",
        "2026-W43-2",
        "invalid",
        "2026-02-29",
        "2026-13-01",
        "2026-10-20T00:00:00",
        " 2026-10-20",
    ],
)
def test_noncanonical_cli_date_is_usage_error_in_subprocess(review_date):
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            json.dumps(dated_payload("2026-03-01")),
            "--as-of",
            review_date,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert result.stderr
    assert not result.stdout


@pytest.mark.parametrize("review_date", ["2026-10-20", "2024-02-29"])
def test_canonical_cli_date_is_accepted_directly(review_date, capsys):
    assert (
        read_file_main([json.dumps(dated_payload(review_date)), "--as-of", review_date])
        == 0
    )
    captured = capsys.readouterr()
    assert not captured.err
    output = json.loads(captured.out)
    assert output["read_as_of"] == review_date
    assert output["status"] == "MAINTAINED"


@pytest.mark.parametrize("review_date", ["2026-10-20", "2024-02-29"])
def test_canonical_cli_date_is_accepted_in_subprocess(review_date):
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            json.dumps(dated_payload(review_date)),
            "--as-of",
            review_date,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert not result.stderr
    output = json.loads(result.stdout)
    assert output["read_as_of"] == review_date
    assert output["status"] == "MAINTAINED"


@pytest.mark.parametrize("review_date", ["20261020", "2026-W43-2"])
def test_library_review_date_keeps_broader_iso_normalization(review_date):
    file = CommitmentFile("library date", frozenset({"code"}), frozenset(CODE_SIGNALS))
    assert read_file(file, as_of=review_date) == read_file(file, as_of="2026-10-20")
