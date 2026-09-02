"""Frozen record types for commitments, declared files, and readings."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import CommitmentKind, FileStatus, StewardshipStatus


@dataclass(frozen=True)
class Commitment:
    """One keepable wire: a commitment, its tags, and required care signals.

    ``required_signals`` names the evidence labels a steward could declare to
    show the commitment was tended. The registry is a method instrument: it
    describes how to keep working on what exists and never guarantees that
    anything is maintained.
    """

    id: str
    title: str
    wire: str
    tags: frozenset[str]
    required_signals: tuple[str, ...]
    kind: CommitmentKind = CommitmentKind.SYSTEM

    def canonical(self) -> dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "wire": self.wire,
            "tags": sorted(self.tags),
            "required_signals": list(self.required_signals),
            "kind": self.kind.value,
        }


@dataclass(frozen=True)
class CareSignal:
    """A dated declaration pointing to an act of care.

    ``noted_on`` is an ISO date string recording when the care was last
    recorded. Undated signals (``noted_on is None``) are treated as current
    declarations; the evaluator does not independently verify them.
    """

    label: str
    noted_on: str | None = None


@dataclass(frozen=True)
class CommitmentFile:
    """A self-declared file of commitments assessed against the registry.

    ``tags`` selects which commitments apply; ``evidence`` and
    ``dated_evidence`` declare care signals, undated and dated respectively.
    """

    description: str
    tags: frozenset[str] = frozenset()
    evidence: frozenset[str] = frozenset()
    dated_evidence: tuple[CareSignal, ...] = ()


@dataclass(frozen=True)
class CommitmentFinding:
    """One commitment-level declaration status with a reviewable reason trail."""

    commitment_id: str
    status: StewardshipStatus
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class SignalSurfaces:
    """One commitment's care and neglect, co-present and typed.

    A finding's status is a projection. The surfaces keep what the projection
    compresses: required signals declared fresh (``present``), required
    signals not declared (``missing``), and the subset of missing that is
    merely stale (``stale``). All three tuples follow the commitment's
    declared signal order, and ``stale`` is always a subset of ``missing``.
    A present label is a declaration, never verified care.
    """

    commitment_id: str
    present: tuple[str, ...]
    missing: tuple[str, ...]
    stale: tuple[str, ...]


@dataclass(frozen=True)
class StewardshipReading:
    """A complete reading, including the commitments that applied."""

    status: FileStatus
    findings: tuple[CommitmentFinding, ...]
    intake_notes: tuple[str, ...] = ()
    read_as_of: str = ""
    registry_version: str = ""
    registry_digest: str = ""
