"""Thin CLI: read one declared commitment file described as JSON on argv.

The JSON object mirrors CommitmentFile fields (description, tags, evidence,
dated_evidence). Prints the verdict and per-commitment findings as JSON.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line.cli import read_file_main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(read_file_main())
