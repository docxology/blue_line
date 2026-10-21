"""Figure specifications for the Blue Line instrument.

Each spec names a figure the builder can emit deterministically from repo
data. Specs carry no numbers; every value is derived at build time.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FigureSpec:
    """One emit-able figure: an id, a title, and a description."""

    figure_id: str
    title: str
    description: str

    @property
    def label(self) -> str:
        """The manuscript-facing ``fig:`` label, derived from the id."""

        return "fig:" + self.figure_id.replace("_", "-")


FIGURE_SPECS: tuple[FigureSpec, ...] = (
    FigureSpec(
        "blue_registry_map",
        "Commitment registry map",
        "Every registry commitment grouped by kind, with its required care signals.",
    ),
    FigureSpec(
        "blue_verdict_paths",
        "Verdict paths",
        "How declared and missing care signals resolve to each verdict state.",
    ),
    FigureSpec(
        "blue_freshness_window",
        "Signal freshness window",
        "Declared freshness policy, renewal precedence, unreadable intake dates and future-date review diagnostics; historical example date only.",
    ),
    FigureSpec(
        "blue_line_cover",
        "Cover plate",
        "Symbolic strokes along tracks: a stewardship motif, encoding no registry counts or measured maintenance.",
    ),
)


def figure_ids() -> tuple[str, ...]:
    """Return the figure ids in declaration order."""

    return tuple(spec.figure_id for spec in FIGURE_SPECS)
