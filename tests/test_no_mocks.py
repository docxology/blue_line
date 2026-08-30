"""The no-mocks gate: no mocking framework may appear anywhere in the repo."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

FORBIDDEN = (
    "unittest.mock",
    "MagicMock",
    "mocker.patch",
    "mock.patch",
    "AsyncMock",
    "patch(",
)


def test_no_mock_framework_anywhere():
    offenders: list[str] = []
    for tree in ("src", "tests", "scripts"):
        for path in sorted((REPO / tree).rglob("*.py")):
            if path.name == "test_no_mocks.py":
                continue
            text = path.read_text(encoding="utf-8")
            for needle in FORBIDDEN:
                if needle in text:
                    offenders.append(f"{path.relative_to(REPO)}: {needle}")
    assert offenders == []
