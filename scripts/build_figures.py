"""Build the Blue Line figures into output/figures."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blue_line.figures import build_all, build_cover_png, figure_ids  # noqa: E402


def main() -> int:
    out_dir = Path(__file__).resolve().parents[1] / "output" / "figures"
    emitted = build_all(out_dir)
    for figure_id in figure_ids():
        print(f"built {figure_id} -> {out_dir / emitted[figure_id]}")
    cover_png = build_cover_png(out_dir)
    print(f"built {cover_png.name} -> {cover_png}")
    print(f"built {len(emitted)} figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
