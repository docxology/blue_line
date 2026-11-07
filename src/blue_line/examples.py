"""Regenerate prepared declarations and companion reports; no sibling admission."""

from __future__ import annotations

import json
from pathlib import Path

from .envelope import build_envelope, envelope_digest
from .evaluator import read_with_surfaces
from .json_adapter import declaration_from_json
from .report import build_report


def write_examples(repo: Path) -> tuple[Path, ...]:
    """Derive outputs only from declarations and explicit example contexts."""
    contexts = json.loads((repo / "data/example_contexts.json").read_text(encoding="utf-8"))
    emitted: list[Path] = []
    for source in sorted((repo / "data" / "declared_files").glob("*.json")):
        target = repo / "data" / "envelopes" / source.name
        context = contexts[source.name]
        reading, surfaces = read_with_surfaces(
            declaration_from_json(json.loads(source.read_text(encoding="utf-8"))),
            as_of=context["review_date"],
        )
        envelope = build_envelope(reading, subject_id=context["subject_id"],
                                  source_snapshot_refs=tuple(context["source_snapshot_refs"]))
        report = build_report(reading, surfaces)
        binding = {
            "schema_version": "blue_line.report-binding/1.0",
            "envelope_digest": envelope_digest(envelope),
            "projection_digest": report["projection_digest"],
            "replay_digest": report["replay_digest"],
            "report_path": f"data/reports/{source.name}",
        }
        for path, data in ((target, envelope), (repo / "data/reports" / source.name, report),
                           (repo / "data/report_bindings" / source.name, binding)):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            emitted.append(path)
    return tuple(emitted)
