"""The public API surface exports what the docs promise."""

from __future__ import annotations

import blue_line


def test_version_exposed():
    assert isinstance(blue_line.__version__, str) and blue_line.__version__


def test_all_names_importable():
    missing = [name for name in blue_line.__all__ if not hasattr(blue_line, name)]
    assert missing == []


def test_line_identity():
    assert blue_line.BLUE_LINE_ID == "blue_line"


def test_scope_and_nonclaims_nonempty():
    assert blue_line.SCOPE_AND_NONCLAIMS
    assert any("not a maintenance" in c for c in blue_line.SCOPE_AND_NONCLAIMS)
