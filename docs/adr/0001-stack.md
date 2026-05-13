# ADR 0001: Initial Technical Stack

Status: proposed

## Decision

Use FastAPI, PostgreSQL, Redis, Keycloak, OPA, Next.js, and a custom append-only journal for the first implementation.

## Context

`stack.md`, `TechnicalTask.md`, and `Plan_1.md` recommend a modular monolith first, with strong boundaries and verifiable civic procedures before broad infrastructure expansion.

## Consequences

- The first implementation can be developed and operated with Docker Compose.
- AI, media, OpenSearch, Qdrant, NATS, and Kubernetes remain staged additions.
- The journal/verifier path must be implemented early because it is central to public trust.

