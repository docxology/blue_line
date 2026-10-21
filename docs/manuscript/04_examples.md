# Examples

## A maintained quarter

A declared file describing the line-set reader, tagged code and docs,
declaring every required signal for the applicable commitments. The reading
returns per-commitment findings; where all signals were declared fresh the
finding is MAINTAINED. The verdict describes declarations, not health.

## A stale repository

The same file with every signal dated 2025-01-01, read at 2026-08-01. Every
signal is older than the configured default window, so the applicable commitments read
STALE and the file verdict is STALE. Nothing failed; nobody visited.

## An unmatched scan

A file tagged only data, declaring nothing. No commitment matches, the
verdict is OUTSIDE_SCOPE, and the note reads that nothing was read. The
instrument declines to manufacture an opinion.

## Renewal and a future declaration

A stale declaration of a label can coexist with a fresh or undated renewal.
Fresh membership takes precedence; only the effective stale subset remains
missing. A future-only declaration is excluded at the resolved review date
and receives a review diagnostic. Neither case establishes that care happened.
