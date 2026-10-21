"""Public Blue Line API."""

from . import envelope as envelope_module
from .enums import CommitmentKind, FileStatus, StewardshipStatus
from .evaluator import invariants_hold, read_file, read_with_surfaces
from .figures import FIGURE_SPECS, FigureSpec, build_all, figure_ids
from .records import (
    CareSignal,
    Commitment,
    CommitmentFile,
    CommitmentFinding,
    EvaluationContext,
    SignalSurfaces,
    StewardshipReading,
)
from .registry import BLUE_COMMITMENTS, COMMITMENT_TAG_VOCABULARY, registry_ids
from .serialization import (
    canonical_reading,
    canonical_registry,
    reading_digest,
    registry_digest,
)
from .version import __version__
from .report import build_report, replay_report, stewardship_worklist
from .serialization import context_digest, replay_digest
from .envelope import EnvelopeEligibilityError, envelope_digest
from .validation import validate_registry

BLUE_LINE_ID = envelope_module.BLUE_LINE_ID
ENVELOPE_SCHEMA = envelope_module.ENVELOPE_SCHEMA
SCOPE_AND_NONCLAIMS = envelope_module.SCOPE_AND_NONCLAIMS
build_envelope = envelope_module.build_envelope
envelope_matches_reading = envelope_module.envelope_matches_reading

__all__ = [
    "BLUE_COMMITMENTS",
    "BLUE_LINE_ID",
    "COMMITMENT_TAG_VOCABULARY",
    "CareSignal",
    "Commitment",
    "CommitmentFile",
    "CommitmentFinding",
    "CommitmentKind",
    "ENVELOPE_SCHEMA",
    "EnvelopeEligibilityError",
    "EvaluationContext",
    "FIGURE_SPECS",
    "FileStatus",
    "FigureSpec",
    "SCOPE_AND_NONCLAIMS",
    "SignalSurfaces",
    "StewardshipReading",
    "StewardshipStatus",
    "__version__",
    "build_all",
    "build_envelope",
    "build_report",
    "canonical_reading",
    "canonical_registry",
    "context_digest",
    "envelope_digest",
    "envelope_matches_reading",
    "figure_ids",
    "invariants_hold",
    "read_file",
    "read_with_surfaces",
    "replay_report",
    "replay_digest",
    "reading_digest",
    "registry_digest",
    "registry_ids",
    "stewardship_worklist",
    "validate_registry",
]
