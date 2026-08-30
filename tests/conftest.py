"""Shared fixtures: real files, real temp dirs, no mocks."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from blue_line.records import CareSignal, CommitmentFile  # noqa: E402

REVIEW_DATE = "2026-08-01"

CODE_DOCS_SIGNALS = (
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
)


@pytest.fixture
def review_date() -> str:
    return REVIEW_DATE


@pytest.fixture
def maintained_file() -> CommitmentFile:
    """A code+docs file declaring every required signal fresh."""

    return CommitmentFile(
        description="the docxology line-set reader under stewardship",
        tags=frozenset({"code", "docs"}),
        evidence=frozenset(CODE_DOCS_SIGNALS),
    )


@pytest.fixture
def stale_file() -> CommitmentFile:
    """A code+docs file whose dated signals all aged past the window."""

    return CommitmentFile(
        description="an aging repo nobody has visited this year",
        tags=frozenset({"code", "docs"}),
        dated_evidence=tuple(
            CareSignal(label=label, noted_on="2025-01-01")
            for label in CODE_DOCS_SIGNALS
        ),
    )


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    return tmp_path / "figures"
