# ADR 0002: Journal-First Civic State

Status: proposed

## Decision

Authoritative civic state transitions must be appended to a tamper-evident journal. Relational tables, search indexes, public pages, and dashboards are projections or interfaces.

## Consequences

- Important workflows must fail closed if journal append fails.
- Journal exports need independent verification tooling.
- Raw personal data should not be written to public journal records.

