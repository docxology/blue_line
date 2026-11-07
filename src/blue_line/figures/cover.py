"""The cover plate: Blue Line's title-page figure.

The plate is a symbolic motif of strokes kept along tracks. Its geometry
does not encode registry membership, counts, kinds or measured maintenance.
The SVG is stable for its fixed drawing constants; PNG bytes additionally
depend on renderer, fonts and environment.

The canvas matches the sibling covers' title-page proportions (a 1800x1100
viewBox). The two labels are the only visible text; the palette is the
house cream canvas carried by the Line Set figure modules. The local ``BLUE``
constant defines this work's stroke and matches the set's muted
``COVER_STROKE["blue"]`` palette value; no sibling import is required.
"""

from __future__ import annotations

WIDTH = 1800
HEIGHT = 1100

#: House canvas and inks, shared with the Line Set figure modules.
PAPER = "#f4f1ea"
INK = "#22201d"
MUTED = "#6c655c"
RULE = "#c6bdae"

#: The register's tracks: a step darker than the frame rule so a kept
#: stroke always reads as a fill on a named span, even at embed scale.
TRACK = "#ada28d"

#: This work's stroke: the muted stand-in the set's palette carries for blue.
BLUE = "#3465a4"

#: The visible labels. Nothing else may appear on the plate.
TITLE = "BLUE LINE"
TAGLINE = "MAINTAINED COMMITMENTS, KEPT IN TRUST"

#: Frame inset and title metrics.
_FRAME = 44.0
_TITLE_X = 96.0
_TITLE_Y = 150.0
_TITLE_SIZE = 46
_TITLE_RULE_Y = 176.0
_TITLE_RULE_END = 352.0

#: The horizon: the dominant stroke the register is kept against.
_HORIZON_Y = 300.0

#: Symbolic bands; their geometry carries no registry counts.
_BAND_YS = (440.0, 570.0, 700.0, 830.0)
_ROW_STEP = 34.0
_TRACK_START = 180.0
_TRACK_END = 1672.0

#: Stroke lengths cycle arithmetically, so the register is rhythmic but
#: never repeats one pattern long enough to read as accidental. A stroke
#: ends at most at 1660, so its dot always sits inside the track.
_LENGTHS = (1480.0, 1230.0, 1350.0, 1120.0, 1440.0, 1290.0)


def _band(index: int) -> str:
    """Draw one symbolic band of strokes over shared tracks."""

    parts: list[str] = []
    for row in range(3):
        stroke_y = _BAND_YS[index] + row * _ROW_STEP
        parts.append(
            f'<line x1="{_TRACK_START:.0f}" y1="{stroke_y:.0f}" '
            f'x2="{_TRACK_END:.0f}" y2="{stroke_y:.0f}" '
            f'stroke="{TRACK}" stroke-width="2.5"/>'
        )
        length = _LENGTHS[(index * 3 + row) % len(_LENGTHS)]
        end = _TRACK_START + length
        parts.append(
            f'<line x1="{_TRACK_START:.0f}" y1="{stroke_y:.0f}" '
            f'x2="{end:.0f}" y2="{stroke_y:.0f}" stroke="{BLUE}" '
            f'stroke-width="8" stroke-linecap="round"/>'
        )
        parts.append(
            f'<circle cx="{end:.0f}" cy="{stroke_y:.0f}" r="10" fill="{BLUE}"/>'
        )
    return "".join(parts)


def cover_svg() -> str:
    """Render the cover: the kept register of maintained commitments."""

    body = [
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        f'<rect x="{_FRAME:.0f}" y="{_FRAME:.0f}" '
        f'width="{WIDTH - 2 * _FRAME:.0f}" height="{HEIGHT - 2 * _FRAME:.0f}" '
        f'fill="none" stroke="{RULE}" stroke-width="2"/>',
        f'<text x="{_TITLE_X:.0f}" y="{_TITLE_Y:.0f}" font-family="serif" '
        f'font-size="{_TITLE_SIZE}" font-weight="700" letter-spacing="10" '
        f'fill="{INK}">{TITLE}</text>',
        f'<line x1="{_TITLE_X:.0f}" y1="{_TITLE_RULE_Y:.0f}" '
        f'x2="{_TITLE_RULE_END:.0f}" y2="{_TITLE_RULE_Y:.0f}" '
        f'stroke="{BLUE}" stroke-width="6"/>',
        f'<line x1="{_TITLE_X:.0f}" y1="{_HORIZON_Y:.0f}" '
        f'x2="{WIDTH - _TITLE_X:.0f}" y2="{_HORIZON_Y:.0f}" stroke="{BLUE}" '
        f'stroke-width="14" stroke-linecap="round"/>',
    ]
    for band in range(len(_BAND_YS)):
        body.append(_band(band))
    body.append(
        f'<text x="{WIDTH - 96}" y="980" font-family="serif" font-size="22" '
        f'font-weight="700" letter-spacing="4" fill="{MUTED}" '
        f'text-anchor="end">{TAGLINE}</text>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-labelledby="cover-title cover-desc">'
        f'<title id="cover-title">Blue Line: a stewardship instrument for '
        f"maintained commitments</title>"
        f'<desc id="cover-desc">Symbolic blue strokes along tracks under a '
        f"horizon line. The motif encodes no registry counts or measured "
        f"maintenance.</desc>"
        f"{''.join(body)}</svg>"
    )


__all__ = ["cover_svg"]
