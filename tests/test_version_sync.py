"""Package version and pyproject stay in lockstep."""

from __future__ import annotations

import tomllib
from pathlib import Path

import blue_line

REPO = Path(__file__).resolve().parents[1]


def test_version_matches_pyproject():
    data = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["version"] == blue_line.__version__


def test_version_file_is_authority():
    from blue_line.version import __version__ as v

    assert blue_line.__version__ == v
