"""Enumerations for stewardship verdicts and commitment families.

The Blue Line answers one question — what must I keep working? — and its
verdicts describe the declaration state of maintained commitments. They
never certify that a commitment is healthy, that an obligation is discharged,
or that a relationship is sound.
"""

from __future__ import annotations

from enum import Enum


class StewardshipStatus(str, Enum):
    """Outcome for a single commitment that applies to a declared file."""

    MAINTAINED = "MAINTAINED"
    NEEDS_ATTENTION = "NEEDS_ATTENTION"
    STALE = "STALE"


class FileStatus(str, Enum):
    """Overall outcome for a declared commitment file."""

    MAINTAINED = "MAINTAINED"
    NEEDS_ATTENTION = "NEEDS_ATTENTION"
    STALE = "STALE"
    OUTSIDE_SCOPE = "OUTSIDE_SCOPE"


class CommitmentKind(str, Enum):
    """The family of maintained commitment a registry entry names.

    Families exist so the registry can be reviewed for balance: a registry
    that only watches systems but never relationships has drifted from the
    Blue Line's purpose of stewarding the whole relationship to past work.
    """

    SYSTEM = "SYSTEM"
    OBLIGATION = "OBLIGATION"
    RELATIONSHIP = "RELATIONSHIP"
    ARTIFACT = "ARTIFACT"
