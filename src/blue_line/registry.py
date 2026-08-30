"""The versioned Blue Line commitment registry.

Every entry names one keepable commitment, the tags that make it applicable,
and the care signals a steward could declare. The registry is a method
instrument: it describes how to keep working on what exists and never grants
a warranty, SLA, availability guarantee, or proof of maintenance.
"""

from __future__ import annotations

from .enums import CommitmentKind
from .records import Commitment

#: The reviewed tag vocabulary. Commitment tags outside this set are
#: unreviewable drift; the invariants battery enforces membership.
COMMITMENT_TAG_VOCABULARY: frozenset[str] = frozenset(
    {"code", "docs", "data", "community", "infrastructure"}
)


BLUE_COMMITMENTS: tuple[Commitment, ...] = (
    Commitment(
        "documented-handover",
        "Record how to continue the work",
        "A steward leaving a commitment behind leaves instructions a successor can follow.",
        frozenset({"code", "docs"}),
        ("handover_note", "run_instructions"),
        CommitmentKind.ARTIFACT,
    ),
    Commitment(
        "working-verification",
        "Keep a runnable check for every live commitment",
        "A maintained commitment can be exercised; the check that proves it still runs.",
        frozenset({"code", "infrastructure"}),
        ("check_run", "check_result"),
        CommitmentKind.SYSTEM,
    ),
    Commitment(
        "honest-status-signal",
        "State the commitment's real condition",
        "Record condition as it is, including decay, so the next decision starts from truth.",
        frozenset({"code", "docs", "infrastructure"}),
        ("status_note",),
        CommitmentKind.RELATIONSHIP,
    ),
    Commitment(
        "kept-promise-ledger",
        "Track obligations you have accepted",
        "An accepted obligation is recorded with its state so it cannot silently lapse.",
        frozenset({"community", "docs"}),
        ("obligation_entry",),
        CommitmentKind.OBLIGATION,
    ),
    Commitment(
        "response-within-window",
        "Answer commitments made to people",
        "Relationships to past work include the people who rely on it; respond inside the stated window.",
        frozenset({"community"}),
        ("response_log",),
        CommitmentKind.RELATIONSHIP,
    ),
    Commitment(
        "dependency-notice",
        "Notice what your work depends on and what depends on it",
        "Stewardship looks both directions: upstream drift and downstream reliance are both watched.",
        frozenset({"code", "infrastructure"}),
        ("dependency_review", "downstream_list"),
        CommitmentKind.SYSTEM,
    ),
    Commitment(
        "decay-triage",
        "Triage decay before it compounds",
        "Scheduled attention to aging work keeps small rot from becoming abandonment.",
        frozenset({"code", "data", "docs"}),
        ("triage_log",),
        CommitmentKind.SYSTEM,
    ),
    Commitment(
        "archival-honesty",
        "Retire commitments in the record, not in silence",
        "A ended commitment is marked ended, with its final state recorded where successors look.",
        frozenset({"docs", "community"}),
        ("retirement_note",),
        CommitmentKind.ARTIFACT,
    ),
    Commitment(
        "continuity-notes",
        "Leave notes for the future self who inherits the work",
        "The steward's own return is a relationship to past work; record context the returning self needs.",
        frozenset({"docs", "data"}),
        ("continuity_note",),
        CommitmentKind.RELATIONSHIP,
    ),
    Commitment(
        "cared-for-data",
        "Keep recorded data usable for the next reader",
        "Data under stewardship stays findable, described, and loadable, or its limits are stated.",
        frozenset({"data"}),
        ("data_check", "data_description"),
        CommitmentKind.ARTIFACT,
    ),
    Commitment(
        "review-before-reliance",
        "Re-examine a maintained thing before others rely on it again",
        "Prior correctness does not survive drift; re-run, re-read, and re-decide before reuse.",
        frozenset({"code", "data", "infrastructure"}),
        ("review_note", "rerun_result"),
        CommitmentKind.OBLIGATION,
    ),
    Commitment(
        "stated-care-window",
        "Declare how often each commitment is visited",
        "A stated visit cadence makes neglect observable instead of invisible.",
        frozenset({"code", "docs", "community", "infrastructure", "data"}),
        ("cadence_statement",),
        CommitmentKind.RELATIONSHIP,
    ),
)


def registry_ids() -> tuple[str, ...]:
    """Return the registry ids in declaration order."""

    return tuple(commitment.id for commitment in BLUE_COMMITMENTS)
