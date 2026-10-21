from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--template-root", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(args.template_root.resolve()))
    from infrastructure.rendering.manuscript_injection import write_resolved_manuscript_tree
    from infrastructure.rendering.pipeline import execute_render_pipeline

    variables = json.loads((root / "output/data/manuscript_variables.json").read_text())
    write_resolved_manuscript_tree(root, {key.upper(): str(value) for key, value in variables.items()})
    raise SystemExit(execute_render_pipeline("working/blue_line", repo_root=args.template_root.resolve()))
