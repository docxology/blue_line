"""Versioned replay of staged declarations, with retained intake diagnostics.

Replay verifies calculation and content identity, not source authenticity,
the truth of intake diagnostics, references, or any underlying care.
"""

from __future__ import annotations

from dataclasses import asdict, replace

from .evaluator import read_with_surfaces
from .json_adapter import DeclarationShapeError, declaration_from_json
from .records import Commitment, SignalSurfaces, StewardshipReading
from .registry import BLUE_COMMITMENTS
from .serialization import canonical_input, canonical_reading, content_digest, context_digest, replay_digest
from .version import __version__

REPORT_SCHEMA = "blue_line.report/1.0"


class ReportReplayError(ValueError):
    def __init__(self, field: str) -> None:
        self.field = field
        super().__init__(f"{field}: report is incomplete, incompatible, or differs from replay")


def build_report(reading: StewardshipReading, surfaces: tuple[SignalSurfaces, ...]) -> dict[str, object]:
    """Store staged input and policy beside a named legacy projection."""
    if reading.context is None or reading.normalized_input is None:
        raise ReportReplayError("reading")
    return {
        "schema_version": REPORT_SCHEMA,
        "input": canonical_input(reading.normalized_input),
        "context": asdict(reading.context),
        "context_digest": context_digest(reading.context),
        "registry_version": reading.registry_version,
        "projection": canonical_reading(reading),
        "projection_digest": content_digest(canonical_reading(reading)),
        "replay_digest": replay_digest(reading),
        "review_notes": list(reading.review_notes),
        "surfaces": [{"commitment_id": s.commitment_id, "present": list(s.present),
                      "missing": list(s.missing), "stale": list(s.stale)} for s in surfaces],
    }


def replay_report(payload: object, *, commitments: tuple[Commitment, ...] = BLUE_COMMITMENTS
                  ) -> tuple[StewardshipReading, tuple[SignalSurfaces, ...]]:
    """Re-evaluate normalized input; retain the original intake transcript."""
    if not isinstance(payload, dict) or payload.get("schema_version") != REPORT_SCHEMA:
        raise ReportReplayError("schema_version")
    context = payload.get("context")
    projection = payload.get("projection")
    if not isinstance(context, dict) or not isinstance(projection, dict):
        raise ReportReplayError("context/projection")
    if context.get("evaluator_version") != __version__ or payload.get("registry_version") != __version__:
        raise ReportReplayError("evaluator_version")
    window = context.get("max_signal_age_days")
    unknown = context.get("allow_unknown_tags")
    review_date = context.get("read_as_of")
    notes = projection.get("intake_notes")
    if (not isinstance(window, int) or isinstance(window, bool) or window < 0
        or not isinstance(unknown, bool) or not isinstance(review_date, str)
        or not isinstance(notes, list) or any(not isinstance(n, str) for n in notes)):
        raise ReportReplayError("policy/intake_notes")
    try:
        file = declaration_from_json(payload.get("input"))
        reading, surfaces = read_with_surfaces(file, commitments=commitments, as_of=review_date,
            max_signal_age_days=window, allow_unknown_tags=unknown)
    except (DeclarationShapeError, ValueError) as error:
        raise ReportReplayError("input/context") from error
    reading = replace(reading, intake_notes=tuple(notes))
    if build_report(reading, surfaces) != payload:
        raise ReportReplayError("content")
    return reading, surfaces


def stewardship_worklist(reading: StewardshipReading, surfaces: tuple[SignalSurfaces, ...]
                         ) -> tuple[dict[str, object], ...]:
    """Project missing declarations, with optional file-level declared metadata."""
    file = reading.normalized_input
    return tuple({
        "commitment_id": surface.commitment_id,
        "signal": signal,
        "declaration_status": "stale" if signal in surface.stale else "missing",
        "declared_owner": file.declared_owner if file else None,
        "declared_next_review": file.declared_next_review if file else None,
        "source_reference": file.source_reference if file else None,
    } for surface in sorted(surfaces, key=lambda s: s.commitment_id) for signal in sorted(surface.missing))
