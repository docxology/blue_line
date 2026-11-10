"""Fail-closed staged intake for declared commitment files.

Intake runs before evaluation so hostile or malformed input (non-string
labels, unreadable dates, a blank description, an unknown tag) is set aside
with notes instead of crashing or inventing values. An empty scan set is an
outcome, never an exception: the caller receives a read that reports the
vacancy.
"""

from __future__ import annotations

from datetime import date

from .enums import FileStatus
from .records import CareSignal, CommitmentFile
from .registry import COMMITMENT_TAG_VOCABULARY


def _clean_labels(raw: object, field: str) -> tuple[frozenset[str], tuple[str, ...]]:
    """Normalize a declared label collection without letting bad input crash.

    Returns the kept labels (stripped, lowercased) and intake notes for every
    declaration or token that had to be ignored.
    """

    if not isinstance(raw, (frozenset, set, tuple, list)):
        return frozenset(), (
            f"{field} declaration is not a collection of labels and was ignored",
        )
    kept: set[str] = set()
    notes: list[str] = []
    for token in raw:
        if not isinstance(token, str) or not token.strip():
            notes.append(f"ignored a malformed {field} label")
            continue
        kept.add(token.strip().lower())
    return frozenset(kept), tuple(notes)


def _clean_signals(records: object) -> tuple[tuple[CareSignal, ...], tuple[str, ...]]:
    """Normalize dated care-signal declarations, setting aside bad records."""

    if not isinstance(records, (tuple, list)):
        return (), ("dated care declaration is not a collection of records",)
    kept: list[CareSignal] = []
    notes: list[str] = []
    for item in records:
        try:
            label = getattr(item, "label")
            noted_on = getattr(item, "noted_on")
        except Exception:
            notes.append("ignored a care-signal record with unreadable attributes")
            continue
        if not isinstance(label, str) or not label.strip():
            notes.append("ignored a care-signal record without a usable label")
            continue
        if noted_on is not None:
            if isinstance(noted_on, str):
                try:
                    noted_on = date.fromisoformat(noted_on).isoformat()
                except ValueError:
                    notes.append(
                        f"care signal '{label.strip().lower()}' has an unreadable"
                        " date and was set aside"
                    )
                    continue
            else:
                notes.append(
                    f"care signal '{label.strip().lower()}' has a non-string date"
                    " and was set aside"
                )
                continue
        kept.append(CareSignal(label=label.strip().lower(), noted_on=noted_on))
    return tuple(kept), tuple(notes)


def _clean_description(raw: object) -> tuple[str, tuple[str, ...]]:
    """Return a usable description, or a blocking note for a blank one."""

    if not isinstance(raw, str) or not raw.strip():
        return "", ("description is blank or not text; the file cannot be read",)
    return raw.strip(), ()


def intake(
    raw_file: object, *, allow_unknown_tags: bool = True
) -> tuple[CommitmentFile | None, FileStatus, tuple[str, ...]]:
    """Stage a raw declared file into a :class:`CommitmentFile`.

    Returns ``(file, status, notes)``. ``file`` is ``None`` only when the
    intake is blocking (a blank description). Unknown tags are set aside as
    notes when ``allow_unknown_tags`` is true; when false, an unknown tag
    blocks the file rather than silently narrowing the scan.
    """

    if not isinstance(raw_file, CommitmentFile):
        return (
            None,
            FileStatus.OUTSIDE_SCOPE,
            ("input is not a CommitmentFile record and was not read",),
        )
    notes: list[str] = []
    description, description_notes = _clean_description(raw_file.description)
    notes.extend(description_notes)
    tags, tag_notes = _clean_labels(raw_file.tags, "tag")
    notes.extend(tag_notes)
    unknown = sorted(tags - COMMITMENT_TAG_VOCABULARY)
    if unknown and not allow_unknown_tags:
        return (
            None,
            FileStatus.OUTSIDE_SCOPE,
            tuple(notes) + (f"unknown tags block this read: {', '.join(unknown)}",),
        )
    for tag in unknown:
        notes.append(f"unknown tag '{tag}' was set aside and matched nothing")
    evidence, evidence_notes = _clean_labels(raw_file.evidence, "care signal")
    notes.extend(evidence_notes)
    dated, dated_notes = _clean_signals(raw_file.dated_evidence)
    notes.extend(dated_notes)
    metadata: dict[str, str | None] = {}
    for field in ("declared_owner", "declared_next_review", "source_reference"):
        value = getattr(raw_file, field)
        if value is not None:
            if not isinstance(value, str) or not value.strip():
                notes.append(f"{field} is not nonblank text and was set aside")
                value = None
            else:
                value = value.strip()
                if field == "declared_next_review":
                    try:
                        value = date.fromisoformat(value).isoformat()
                    except ValueError:
                        notes.append(f"{field} is not an ISO date and was set aside")
                        value = None
        metadata[field] = value
    status = FileStatus.OUTSIDE_SCOPE if description == "" else None
    if status is not None:
        return None, status, tuple(sorted(notes))
    return (
        CommitmentFile(
            description=description,
            tags=tags & COMMITMENT_TAG_VOCABULARY,
            evidence=evidence,
            dated_evidence=tuple(sorted(dated, key=lambda s: (s.label, s.noted_on or ""))),
            declared_owner=metadata["declared_owner"],
            declared_next_review=metadata["declared_next_review"],
            source_reference=metadata["source_reference"],
        ),
        FileStatus.OUTSIDE_SCOPE,
        tuple(sorted(notes)),
    )
