"""Strict JSON shape boundary; rejected values never become declarations."""

from __future__ import annotations

from datetime import date

from .records import CareSignal, CommitmentFile


class DeclarationShapeError(ValueError):
    def __init__(self, field: str, requirement: str) -> None:
        self.field = field
        self.requirement = requirement
        super().__init__(f"{field}: {requirement}")


def declaration_from_json(payload: object) -> CommitmentFile:
    """Parse JSON arrays before constructing immutable declaration records."""
    if not isinstance(payload, dict):
        raise DeclarationShapeError("$", "expected an object")
    extra = sorted(set(payload) - {"description", "tags", "evidence", "dated_evidence",
                                 "declared_owner", "declared_next_review", "source_reference"})
    if extra:
        raise DeclarationShapeError("$", f"unknown fields: {', '.join(extra)}")
    description = payload.get("description", "")
    if not isinstance(description, str):
        raise DeclarationShapeError("description", "expected text")
    labels: dict[str, frozenset[str]] = {}
    for field in ("tags", "evidence"):
        values = payload.get(field, [])
        if not isinstance(values, list):
            raise DeclarationShapeError(field, "expected an array of labels")
        for index, value in enumerate(values):
            if not isinstance(value, str) or not value.strip():
                raise DeclarationShapeError(f"{field}[{index}]", "expected a nonblank text label")
        labels[field] = frozenset(values)
    records = payload.get("dated_evidence", [])
    if not isinstance(records, list):
        raise DeclarationShapeError("dated_evidence", "expected an array of records")
    dated: list[CareSignal] = []
    for index, record in enumerate(records):
        field = f"dated_evidence[{index}]"
        if not isinstance(record, dict) or set(record) - {"label", "noted_on"}:
            raise DeclarationShapeError(field, "expected an object with label and optional noted_on")
        label = record.get("label")
        if not isinstance(label, str) or not label.strip():
            raise DeclarationShapeError(f"{field}.label", "expected a nonblank text label")
        noted_on = record.get("noted_on")
        if noted_on is not None:
            if not isinstance(noted_on, str):
                raise DeclarationShapeError(f"{field}.noted_on", "expected an ISO date or null")
            try:
                parsed = date.fromisoformat(noted_on)
            except ValueError as error:
                raise DeclarationShapeError(f"{field}.noted_on", "expected an ISO date") from error
            if parsed.isoformat() != noted_on:
                raise DeclarationShapeError(f"{field}.noted_on", "expected YYYY-MM-DD")
        dated.append(CareSignal(label, noted_on))
    metadata: dict[str, str | None] = {}
    for field in ("declared_owner", "declared_next_review", "source_reference"):
        value = payload.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise DeclarationShapeError(field, "expected nonblank text or null")
        if field == "declared_next_review" and value is not None:
            try:
                parsed = date.fromisoformat(value)
            except ValueError as error:
                raise DeclarationShapeError(field, "expected an ISO date") from error
            if value != parsed.isoformat():
                raise DeclarationShapeError(field, "expected YYYY-MM-DD")
        metadata[field] = value
    return CommitmentFile(description, labels["tags"], labels["evidence"], tuple(dated),
                          metadata["declared_owner"], metadata["declared_next_review"], metadata["source_reference"])
