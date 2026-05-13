# Viche Scaffold Implementation Plan

## Purpose

This plan defines the practical repository scaffolding path for Viche. It is narrower than `Plan_1.md` and `Plan_2.md`: it focuses on creating a clean, testable project base that future implementation work can build on without changing architectural direction.

The scaffold should prove that the chosen stack can run locally, expose typed API contracts, render a web shell, validate policy/schema placeholders, and support later implementation of the Plan 1 civic operating system and Plan 2 hierarchical federation layer.

## Inputs

- `stack.md`
- `Plan_1.md`
- `Plan_2.md`
- `TechnicalTask.md`
- `Architecture.md`
- `AGENTS.md`

## Scaffold Goals

1. Keep the repository buildable from a clean checkout.
2. Keep source directories separated by responsibility.
3. Expose the first API contracts before implementing heavy domain behavior.
4. Make Docker Compose the default local environment.
5. Make tests and typechecks runnable without Docker where possible.
6. Preserve Ukrainian as canonical project language while keeping developer tooling practical in English.
7. Reserve clear extension points for identity, journal, proposal graph, sortition, correspondence, and federation.

## Target Repository Shape

```text
apps/
  web/
services/
  api/
packages/
  schemas/
  policy/
  verifier/
infra/
  compose/
  keycloak/
docs/
  adr/
  api/
  operations/
  security/
```

## Phase S0: Repository Hygiene

Deliverables:

- `.gitignore`
- `.dockerignore`
- root `README.md`
- `LICENSE`
- `AGENTS.md`
- root `package.json`
- root `compose.yaml`
- `.env.example`

Acceptance criteria:

- No generated dependency folders are tracked.
- No local secrets are tracked.
- `README.md` explains local development URLs.
- AGPL-3.0 license is present.

## Phase S1: Backend API Skeleton

Deliverables:

- `services/api/pyproject.toml`
- FastAPI application factory
- `/v1/health`
- `/v1/system`
- `/v1/public/proposals`
- `/v1/public/resolutions`
- `/v1/public/correspondence`
- `/v1/federation/node`
- `/v1/federation/relationship-types`
- `/v1/federation/artifact-types`
- `/v1/federation/inbox/artifacts`
- Alembic baseline files
- pytest tests for core skeleton endpoints
- ruff configuration

Acceptance criteria:

- `.venv/bin/pip install -e 'services/api[dev]'` succeeds.
- `.venv/bin/pytest services/api/tests` passes.
- `.venv/bin/ruff check services/api packages/verifier` passes.
- `curl http://localhost:8000/v1/health` returns API, database, and Redis status when Compose is running.

## Phase S2: Domain Skeleton Contracts

Deliverables:

- Plan 1 module registry in backend domain code.
- Federation node metadata models.
- Federation artifact envelope models.
- Public collection placeholders for proposals, resolutions, and correspondence.
- Reserved module keys:
  - `membership`
  - `journal`
  - `proposals`
  - `sortition`
  - `panels`
  - `resolutions`
  - `correspondence`
  - `notifications`
  - `federation`

Acceptance criteria:

- `/v1/system` lists all reserved modules with status `skeleton`.
- `/v1/federation/node` returns protocol version `viche-federation-0.1`.
- OpenAPI includes all skeleton routes.

## Phase S3: Frontend Web Skeleton

Deliverables:

- Next.js app shell.
- Tailwind configuration.
- typed API client with Zod validation.
- home page that displays:
  - API health
  - Plan 1 core modules
  - Plan 2 federation node metadata

Acceptance criteria:

- `npm install` succeeds on Node 22.
- `npm --workspace apps/web run lint` passes.
- `npm audit --omit=dev` reports zero vulnerabilities.
- `http://localhost:3000` renders the skeleton UI when Compose is running.

## Phase S4: Shared Packages

Deliverables:

- `packages/schemas`
  - `member.register.schema.json`
  - `proposal.submit.schema.json`
  - `federation.artifact-envelope.schema.json`
- `packages/policy`
  - OPA/Rego placeholder rules for proposal submission, moderation, and federation triage.
- `packages/verifier`
  - Python CLI skeleton for journal JSONL verification.

Acceptance criteria:

- schema files are valid JSON.
- policy package has explicit skeleton actions.
- verifier package installs or can be run in later CI.

## Phase S5: Local Infrastructure

Deliverables:

- Docker Compose services:
  - PostgreSQL
  - Redis
  - MinIO
  - Keycloak
  - API
  - Web
- Keycloak development realm import.
- Dockerfiles for API and web.

Acceptance criteria:

- `docker compose config` passes.
- `docker compose build api web` passes.
- `docker compose up -d` starts the stack.
- `docker compose ps` shows API and web running.
- API health is `ok`.
- Web renders and shows `API: ok`.

## Phase S6: CI Skeleton

Deliverables:

- `.github/workflows/ci.yaml`
- backend job:
  - Python 3.12
  - install API dev dependencies
  - ruff
  - pytest
- frontend job:
  - Node 22
  - npm install
  - web typecheck

Acceptance criteria:

- CI matches local commands.
- CI does not require secrets for basic checks.
- CI avoids Docker until container CI is intentionally added.

## Phase S7: Documentation Skeleton

Deliverables:

- ADR placeholders:
  - stack
  - journal-first state
  - identity separation
  - Ukrainian canonical language
- operations placeholders:
  - development
  - sortition runbook
  - correspondence runbook
  - moderation runbook
  - incident response
- security placeholders:
  - threat model
  - disclosure policy
- API placeholder:
  - public API overview

Acceptance criteria:

- New contributors can find architecture decisions and runbook locations.
- Placeholders name the intended operational responsibility clearly.

## Suggested Commit Sequence

1. `Add repository hygiene files`
2. `Scaffold FastAPI service`
3. `Add web app skeleton`
4. `Add shared schema policy and verifier packages`
5. `Add local compose infrastructure`
6. `Add CI workflow`
7. `Add operations and ADR docs`
8. `Expose Plan 1 and federation skeleton endpoints`
9. `Connect web shell to skeleton API`

## Verification Checklist

Run before considering scaffold complete:

```bash
npm install
npm audit --omit=dev
npm --workspace apps/web run lint
python3 -m venv .venv
.venv/bin/pip install -e 'services/api[dev]'
.venv/bin/ruff check services/api packages/verifier
.venv/bin/pytest services/api/tests
docker compose config
docker compose build api web
docker compose up -d
curl -fsS http://localhost:8000/v1/health
curl -fsS http://localhost:8000/v1/system
curl -fsS http://localhost:8000/v1/federation/node
curl -fsS http://localhost:3000
```

## Scaffold Exit Criteria

The project scaffold is complete when:

- a fresh developer can clone the repo and run tests;
- a fresh developer can start the local stack;
- API health, system, public, and federation skeleton endpoints respond;
- the web page renders API-backed skeleton status;
- CI covers backend and frontend basic checks;
- all generated files are ignored;
- no secrets are tracked;
- the repo is pushed to GitHub.

## Next Implementation After Scaffold

After this scaffold is complete, implementation should proceed in this order:

1. membership and identity separation;
2. journal append model;
3. proposal intake and moderation;
4. proposal relation graph;
5. sortition pool freeze and reproducible draw;
6. panel and mandate lifecycle;
7. resolution publication;
8. correspondence follow-up;
9. federation import/export from `Plan_2.md`.
