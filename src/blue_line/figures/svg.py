"""Deterministic SVG emission for Blue Line figures.

The builders draw simple, honest diagrams from derived data. Every emitted
figure is stable byte-for-byte for a given registry and date input: nothing
is sorted by accident, and no ambient time enters a figure unless passed in.
"""

from __future__ import annotations

from ..enums import CommitmentKind
from ..registry import BLUE_COMMITMENTS

_KIND_ORDER = (
    CommitmentKind.SYSTEM,
    CommitmentKind.OBLIGATION,
    CommitmentKind.RELATIONSHIP,
    CommitmentKind.ARTIFACT,
)

_ESCAPES = {"&": "&amp;", "<": "&lt;", ">": "&gt;", chr(34): "&quot;"}


def _esc(text: str) -> str:
    return "".join(_ESCAPES.get(ch, ch) for ch in text)


def registry_map_svg() -> str:
    """Draw the registry as kind-grouped rows of commitments and signals."""

    rows: list[str] = []
    y = 30.0
    for kind in _KIND_ORDER:
        members = [c for c in BLUE_COMMITMENTS if c.kind is kind]
        if not members:
            continue
        rows.append(
            f'<text x="10" y="{y:.1f}" class="kind">{_esc(kind.value)}</text>'
        )
        y += 18.0
        for commitment in sorted(members, key=lambda c: c.id):
            signals = ", ".join(commitment.required_signals)
            rows.append(
                f'<text x="24" y="{y:.1f}" class="entry">'
                f"{_esc(commitment.id)}: {_esc(signals)}</text>"
            )
            y += 16.0
        y += 6.0
    height = y + 10.0
    body = chr(10).join(rows)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="720" '
        f'height="{height:.0f}" viewBox="0 0 720 {height:.0f}">'
        + chr(10)
        + "<style>text{font-family:monospace;font-size:12px;fill:#1e293b}"
        ".kind{font-weight:bold}</style>"
        + chr(10)
        + body
        + chr(10)
        + "</svg>"
        + chr(10)
    )


def verdict_paths_svg() -> str:
    """Draw how signal coverage resolves to each verdict."""

    lines: tuple[tuple[str, str], ...] = (
        ("all required signals declared fresh", "MAINTAINED"),
        ("some signals missing, none stale", "NEEDS_ATTENTION"),
        ("a missing signal aged past the window", "STALE"),
        ("no commitment matched the tags", "OUTSIDE_SCOPE"),
        ("empty scan set", "OUTSIDE_SCOPE (fail closed)"),
    )
    rows = [
        f'<text x="10" y="{30.0 + i * 18.0:.1f}" class="entry">'
        f"{_esc(condition)}: {_esc(verdict)}</text>"
        for i, (condition, verdict) in enumerate(lines)
    ]
    body = chr(10).join(rows)
    height = 30.0 + len(lines) * 18.0 + 10.0
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="720" '
        f'height="{height:.0f}" viewBox="0 0 720 {height:.0f}">'
        + chr(10)
        + "<style>text{font-family:monospace;font-size:12px;fill:#1e293b}</style>"
        + chr(10)
        + body
        + chr(10)
        + "</svg>"
        + chr(10)
    )


def freshness_window_svg(as_of: str = "2026-08-01") -> str:
    """Draw the fresh/stale bands against a fixed review date."""

    bands = (
        ("0 to 180 days", "fresh"),
        ("older than 180 days", "stale"),
        ("unreadable or future date", "set aside at intake"),
    )
    rows = [
        f'<text x="10" y="{30.0 + i * 18.0:.1f}" class="entry">'
        f"{_esc(label)}: {_esc(band)} (as of {_esc(as_of)})</text>"
        for i, (label, band) in enumerate(bands)
    ]
    body = chr(10).join(rows)
    height = 30.0 + len(bands) * 18.0 + 10.0
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="720" '
        f'height="{height:.0f}" viewBox="0 0 720 {height:.0f}">'
        + chr(10)
        + "<style>text{font-family:monospace;font-size:12px;fill:#1e293b}</style>"
        + chr(10)
        + body
        + chr(10)
        + "</svg>"
        + chr(10)
    )
