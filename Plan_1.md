# Viche Implementation Plan 1

## Purpose

This plan turns the current Viche concept, technical task, and stack recommendation into an implementation path for the first serious product version.

The target is not a social network, chat bot, party tool, or blockchain experiment. The target is an open-source, API-first civic deliberation platform with lawful participation, rotating mandates, official follow-up, and cryptographic accountability.

## Source Inputs

Primary technical inputs:

- `stack.md`
- `TechnicalTask.md`
- `Architecture.md`

Project and civic idea references:

- `README.md`
- `AGENTS.md`
- `Маніфест Віче.md`
- `Протокол мандата Віче.md`
- `Viche Public Memorandum.md`

## Core Product Principles

1. Ukrainian is the canonical domain language. Other languages are versioned translations.
2. Legal identity and civic activity are separated.
3. Public verifiability does not require public exposure of personal data.
4. Raw public signals are not the same as deliberative outputs.
5. Mandates are temporary responsibilities, not positions of power.
6. AI may assist search, deduplication, summarization, translation, and moderation queues, but it must not decide membership, sortition, votes, resolutions, or legal risk.
7. The immutable journal is the civic source of truth. Databases, search indexes, APIs, and UIs are projections or interfaces.
8. Telegram, mobile apps, and external clients are adapters, not the source of truth.
9. Avoid electioneering, candidate promotion, unlawful investigation, doxxing, harassment, and claims of state authority.

## Selected MVP Stack

Frontend:

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zod
- i18next, Lingui, or FormatJS

Backend:

- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.0 or SQLModel
- Alembic
- Dramatiq, Celery, or RQ for background jobs

Data and infrastructure:

- PostgreSQL as the system of record projection store
- Redis for cache, queues, rate limits, and short-lived state
- MinIO or S3-compatible object storage for evidence files, exports, and media references
- Keycloak for OIDC/OAuth2 identity brokering
- Open Policy Agent for higher-level policy rules
- Custom append-only journal service with hash chaining, signatures, Merkle checkpoints, and verifier tooling
- PostgreSQL full-text search first; pgvector later for semantic duplicate detection
- Server-Sent Events first; WebSockets only where needed
- Docker Compose for local development and pilot deployment
- Jitsi as an optional media integration after the core workflows exist

Deferred until later:

- Kubernetes, Helm, Argo CD
- OpenSearch or Qdrant
- NATS JetStream
- mobile apps
- Telegram Mini App
- full national eID integrations
- threshold signatures and advanced zero-knowledge credentials
- federation between countries or regional nodes

## Target MVP Scope

The MVP must prove the civic trust pipeline end to end:

1. A member can register, authenticate through Keycloak, accept current terms, and receive a stable internal member ID.
2. The system can keep identity-related records separate from public civic records.
3. A member can submit a civic issue or proposal in Ukrainian.
4. Moderators can review, tag, merge, reject, or relate proposals.
5. The system can represent duplicates, alternatives, dependencies, support, and conflict as graph relations.
6. Operators can create an eligible pool snapshot for a simple pilot arena.
7. The sortition service can run a reproducible draw from that frozen pool.
8. Selected members can accept or decline a temporary mandate.
9. Operators can create a panel, agenda, evidence pack, draft resolution, vote result, and public publication record.
10. Operators can create official correspondence, track deadlines, record responses, and publish follow-up status.
11. Every authoritative state transition is written to the append-only journal.
12. The public portal can show proposals, panel outputs, resolutions, correspondence status, and transparency checkpoints.
13. A verifier CLI can validate journal hash chains and checkpoint consistency for exported records.

## Non-MVP Boundaries

Do not implement these in the first release:

- candidate, party, or election workflows
- public legal-name exposure by default
- direct investigative tooling against private individuals
- custom national identity provider
- custom video stack
- blockchain or token mechanics
- AI-generated official resolutions
- automatic merge decisions without human review
- Kafka or a broad microservice architecture
- mobile app before responsive web works well

## Proposed Repository Layout

```text
apps/
  web/                    # Next.js public portal, member cabinet, operator console
services/
  api/                    # FastAPI modular monolith
  journal/                # append-only journal service, can start as an api module
  worker/                 # background jobs for notifications, search indexing, exports
packages/
  schemas/                # shared JSON Schema/OpenAPI fragments
  verifier/               # public verifier CLI/library
  policy/                 # OPA Rego policy bundles
infra/
  compose/                # local Docker Compose
  keycloak/               # realm exports and local setup
  migrations/             # optional shared db bootstrap if not inside service
docs/
  adr/                    # architecture decision records
  api/                    # generated or curated API documentation
  operations/             # runbooks, backup, incident, release procedures
```

If the first scaffold is kept smaller, `services/journal` and `services/worker` may begin inside `services/api` as internal modules. The important rule is to keep domain boundaries clear from day one.

## Phase 0: Project Foundation

Goal: create a buildable, testable, documented skeleton.

Deliverables:

- Monorepo structure.
- Backend FastAPI service with health endpoint.
- Frontend Next.js app with public shell.
- Docker Compose for PostgreSQL, Redis, MinIO, Keycloak, API, and web.
- Python and TypeScript lint/test/format tooling.
- Alembic migration baseline.
- OpenAPI generation in CI.
- Basic developer documentation.
- Architecture decision records for stack, identity split, journal-first model, and Ukrainian canonical language.

Acceptance criteria:

- `docker compose up` starts the local stack.
- API health endpoint returns database and Redis connectivity status.
- Web app can call the API health endpoint.
- CI runs backend tests, frontend checks, and schema validation.
- No secrets are committed.

## Phase 1: Identity, Membership, and Policy Baseline

Goal: create the member foundation without mixing legal identity into public civic data.

Backend modules:

- identity gateway integration with Keycloak OIDC
- member registry
- consent and terms versioning
- locale and notification preferences
- assurance levels
- pseudonymous public IDs
- administrative roles
- policy decision wrapper around OPA

Initial entities:

- `member`
- `member_profile`
- `identity_assertion`
- `public_identity`
- `consent_record`
- `role_assignment`
- `policy_version`
- `audit_subject`

Key API endpoints:

- `GET /v1/me`
- `POST /v1/members/register`
- `PATCH /v1/members/me/preferences`
- `GET /v1/members/me/consents`
- `POST /v1/members/me/consents`
- `GET /v1/admin/members`

Frontend:

- public landing/read portal shell
- member cabinet shell
- sign-in/sign-out
- profile and preferences
- consent screens
- operator member lookup

Journal requirements:

- member registration
- consent acceptance
- role assignment
- policy version publication

Acceptance criteria:

- A user can sign in through Keycloak and create a member profile.
- Public identity is distinct from internal member ID.
- Admins can assign operator roles.
- Policy decisions are logged with policy version references for high-trust actions.

## Phase 2: Journal Service and Public Verifier

Goal: establish tamper-evident civic state before building too many workflows on mutable tables.

Journal design:

- canonical JSON payload serialization
- sequence numbers
- previous-entry hash
- payload hash
- event type
- actor reference
- timestamp
- key ID
- signature
- redaction profile
- Merkle batch checkpoint

Initial event classes:

- `member.registered`
- `consent.accepted`
- `proposal.submitted`
- `proposal.moderated`
- `proposal.relation.created`
- `eligible_pool.frozen`
- `sortition.run_created`
- `sortition.completed`
- `panel.created`
- `mandate.accepted`
- `resolution.published`
- `correspondence.sent`
- `correspondence.response_recorded`
- `policy.published`

Verifier tooling:

- export journal batch as JSONL
- verify hash chain
- verify signatures
- verify Merkle checkpoint root
- produce human-readable verification report

Acceptance criteria:

- Authoritative actions cannot complete without a journal append.
- Journal records can be exported and independently verified.
- Database edits after journal publication are detectable by projection consistency checks.

## Phase 3: Issue and Proposal Intake

Goal: turn scattered civic input into structured, moderated issue records.

Backend modules:

- arenas and jurisdictions
- issue/proposal submission
- tags and taxonomy
- evidence links and object-storage attachments
- moderation queue
- proposal relation graph
- public read projections
- basic full-text search

Initial entities:

- `arena`
- `territory`
- `issue`
- `proposal`
- `proposal_relation`
- `tag`
- `evidence_bundle`
- `evidence_item`
- `moderation_case`
- `moderation_decision`

Relation types:

- `duplicate_of`
- `near_duplicate_of`
- `alternative_to`
- `supports`
- `conflicts_with`
- `depends_on`
- `supersedes`
- `evidence_for`
- `evidence_against`

Frontend:

- proposal submission form
- proposal detail page
- issue/proposal search
- moderator queue
- merge/relation tools
- public proposal graph view, simple at first

Acceptance criteria:

- Members can submit proposals.
- Moderators can approve, reject, tag, and relate proposals.
- Public users can browse approved proposals.
- Duplicate and alternative relations are visible and reversible.
- Evidence files are stored outside the main database with hashes and provenance.

## Phase 4: Sortition, Mandates, and Panel Lifecycle

Goal: create a reproducible pilot panel from a frozen eligible pool.

Backend modules:

- eligibility snapshot creation
- sortition rulesets
- seed bundle generation
- reproducible draw algorithm
- reserve list management
- mandate invitation and acceptance
- conflict-of-interest declarations
- panel lifecycle state machine

Lifecycle:

```text
candidate_pool_frozen -> invited -> accepted -> seated -> briefed -> deliberating -> drafting -> voting -> published -> follow_up -> archived
```

Initial entities:

- `eligibility_pool`
- `eligibility_pool_member`
- `sortition_ruleset`
- `sortition_run`
- `randomness_source`
- `draw_result`
- `panel`
- `panel_seat`
- `mandate`
- `conflict_of_interest_declaration`

Frontend:

- operator sortition setup
- frozen pool review
- draw transcript page
- member mandate invitation flow
- COI declaration form
- panel roster with public-safe identities

Acceptance criteria:

- Operators can freeze an eligible pool and publish its hash.
- Sortition can be replayed from the published pool hash, policy hash, and seed bundle.
- Selected members can accept or decline.
- Reserve replacement is tracked.
- Panel public roster uses pseudonymous or policy-approved identities.
- All transitions are journaled.

## Phase 5: Deliberation, Resolutions, and Voting

Goal: support a complete panel workflow from agenda to published resolution.

Backend modules:

- agenda management
- evidence pack assembly
- witness and session metadata
- draft resolution workflow
- internal panel voting
- minority notes
- publication and redaction

Initial entities:

- `debate_session`
- `agenda_item`
- `witness`
- `transcript_reference`
- `resolution`
- `resolution_version`
- `vote`
- `vote_tally`
- `minority_note`
- `publication_record`

Frontend:

- panel workspace
- agenda view
- evidence pack view
- draft resolution editor
- panel vote flow
- public resolution page
- operator publication workflow

Acceptance criteria:

- Operators can build an evidence pack and agenda.
- Panelists can review materials and vote on a draft resolution.
- The system preserves vote tally, final text, minority notes, and publication metadata.
- Published resolutions are immutable except for explicit superseding/correction records.

## Phase 6: Official Correspondence and Follow-Up

Goal: make public accountability visible after a recommendation is issued.

Correspondence state machine:

```text
draft -> signed -> sent -> delivery_confirmed -> acknowledged -> answered -> published -> closed
```

Branches:

```text
overdue
rejected
needs_escalation
withdrawn
corrected
```

Initial entities:

- `correspondence`
- `correspondence_target`
- `dispatch_attempt`
- `delivery_receipt`
- `official_response`
- `deadline`
- `followup_status`
- `public_dashboard_metric`

Frontend:

- operator correspondence workflow
- deadline tracker
- response upload and publication
- public follow-up dashboard
- overdue and answered views

Acceptance criteria:

- A published resolution can create one or more official correspondence records.
- Operators can track dispatch, delivery, response, and overdue status.
- Public portal shows current status and history.
- Manual evidence of delivery has confidence level metadata.

## Phase 7: Notifications and Event Feeds

Goal: notify members and operators without making external channels authoritative.

Backend modules:

- notification preferences
- in-app notifications
- email adapter
- critical acknowledgement workflow
- SSE public event streams
- webhook outbox for future integrations

Initial event feeds:

- `proposal.created`
- `proposal.moderated`
- `proposal.merged`
- `panel.seated`
- `mandate.invited`
- `resolution.published`
- `correspondence.deadline_due`
- `correspondence.answered`
- `checkpoint.published`

Acceptance criteria:

- Critical invitations require positive acknowledgement.
- Notifications are retryable and auditable.
- Public SSE streams expose non-sensitive updates.
- Webhook events are signed.

## Phase 8: AI-Assisted Workflows

Goal: add bounded AI assistance after the human and journal workflow exists.

MVP AI functions:

- proposal similarity suggestions
- moderator duplicate candidates
- evidence bundle summarization drafts
- transcript summarization drafts
- translation assistance
- public-safe summary drafts

Required controls:

- model/provider recorded
- input sources recorded
- generated output versioned
- confidence or quality metadata recorded where available
- human review state required before official use
- no AI artifact becomes authoritative by default

Acceptance criteria:

- AI suggestions never directly merge proposals or publish official text.
- Human reviewers can accept, edit, reject, and trace AI drafts.
- Official pages link back to human-approved sources and evidence.

## Phase 9: Media Integration

Goal: support structured deliberation sessions without making video the core product.

MVP integration:

- Jitsi meeting link management
- session schedule
- public stream URL field
- recording URL field
- transcript reference field
- attendance metadata

Deferred:

- automated Jibri orchestration
- built-in livestream hosting
- real-time captions
- custom WebRTC/LiveKit media core

Acceptance criteria:

- A panel session can reference a private meeting, public stream, recording, transcript, agenda, and evidence pack.
- Public pages can show session metadata without exposing private room details.

## Phase 10: Pilot Hardening

Goal: prepare for a serious local pilot.

Security:

- threat model update
- permission review
- rate limits
- CSRF/CORS review
- secret rotation procedure
- dependency scanning
- container scanning
- backup and restore test
- incident response runbook

Observability:

- structured logs
- OpenTelemetry traces
- Prometheus metrics
- Grafana dashboards
- journal append failure alerts
- queue depth alerts
- deadline processing alerts

Release:

- signed container images
- SBOM generation
- release notes
- database migration checklist
- rollback procedure
- public status page plan

Acceptance criteria:

- Restore test succeeds from backup.
- Journal verification is part of release checks.
- Basic load test covers proposal intake, public read pages, and sortition replay.
- Pilot operators have runbooks for moderation, correspondence, and incident response.

## First Data Model Cut

The first database schema should be conservative and relational. Avoid over-modeling future international federation.

Core tables:

- `members`
- `identity_assertions`
- `public_identities`
- `consent_records`
- `roles`
- `role_assignments`
- `arenas`
- `territories`
- `issues`
- `proposals`
- `proposal_relations`
- `evidence_bundles`
- `evidence_items`
- `moderation_cases`
- `eligibility_pools`
- `eligibility_pool_members`
- `sortition_rulesets`
- `sortition_runs`
- `panels`
- `panel_seats`
- `mandates`
- `conflict_declarations`
- `debate_sessions`
- `resolutions`
- `votes`
- `correspondence`
- `official_responses`
- `deadlines`
- `journal_entries`
- `journal_checkpoints`
- `outbox_events`
- `notifications`

PII-bearing tables should be isolated by schema, encryption policy, access policy, and backup handling.

## Initial API Surface

Commands:

- `POST /v1/members/register`
- `POST /v1/proposals`
- `POST /v1/proposals/{id}/relations`
- `POST /v1/moderation/cases/{id}/decide`
- `POST /v1/eligibility-pools`
- `POST /v1/sortitions`
- `POST /v1/sortitions/{id}/run`
- `POST /v1/mandates/{id}/accept`
- `POST /v1/mandates/{id}/decline`
- `POST /v1/panels`
- `POST /v1/resolutions`
- `POST /v1/resolutions/{id}/votes`
- `POST /v1/resolutions/{id}/publish`
- `POST /v1/correspondence`
- `POST /v1/correspondence/{id}/responses`

Reads:

- `GET /v1/me`
- `GET /v1/public/proposals`
- `GET /v1/public/proposals/{id}`
- `GET /v1/public/panels`
- `GET /v1/public/resolutions`
- `GET /v1/public/correspondence`
- `GET /v1/public/checkpoints`
- `GET /v1/admin/moderation/cases`
- `GET /v1/admin/deadlines`

Streams:

- `GET /v1/stream/public`
- `GET /v1/stream/arena/{arena_id}`
- `GET /v1/stream/panel/{panel_id}`

## Testing Strategy

Backend:

- unit tests for domain services
- integration tests against PostgreSQL and Redis
- Alembic migration tests
- policy tests for OPA decisions
- journal hash-chain tests
- property tests for sortition replay
- API contract tests from OpenAPI

Frontend:

- component tests for forms and stateful controls
- E2E tests for key user flows
- accessibility checks
- localization smoke tests

Verifier:

- known-good journal fixtures
- tampered-entry fixtures
- missing-entry fixtures
- invalid-signature fixtures
- checkpoint mismatch fixtures

Operational:

- backup restore drill
- migration rollback drill
- minimal load test
- dependency and container scan in CI

## Implementation Order for the First 12 Weeks

Weeks 1-2:

- scaffold monorepo
- Docker Compose stack
- backend health/API shell
- frontend shell
- database migration baseline
- Keycloak local realm
- CI basics

Weeks 3-4:

- member registration
- OIDC login
- consent records
- public identity split
- role assignments
- OPA wrapper
- first journal entry format

Weeks 5-6:

- proposal intake
- arenas and territories
- moderation queue
- proposal relations
- public proposal pages
- evidence upload metadata

Weeks 7-8:

- journal signing and verification
- journal export
- verifier CLI
- sortition rulesets
- eligible pool freeze
- reproducible draw prototype

Weeks 9-10:

- mandate invitation and acceptance
- panel creation
- COI declaration
- agenda/evidence pack basics
- resolution draft and vote basics

Weeks 11-12:

- resolution publication
- correspondence state machine
- public follow-up dashboard
- notification basics
- pilot hardening checklist

## Pilot Definition of Done

The first pilot is ready when Viche can run this complete demonstration without manual database edits:

1. Register 100-1,000 pilot members.
2. Accept terms and language preferences.
3. Submit 50-200 proposals.
4. Moderate, tag, and relate proposals.
5. Freeze an eligible pool.
6. Run and replay a sortition.
7. Seat a panel with accepted mandates.
8. Publish an agenda and evidence pack.
9. Record a panel vote and resolution.
10. Send or record official correspondence.
11. Track response deadline and status.
12. Export and verify the journal.
13. Show all public-safe outputs in the public portal.

## Main Risks

Legal perimeter:

- Mitigation: review electioneering, NGO, personal-data, and correspondence rules before production pilot.

Identity integration access:

- Mitigation: start with Keycloak and internal assurance levels; add BankID, Diia.Signature, and KEP adapters after provider access is confirmed.

Trust pipeline complexity:

- Mitigation: implement simple hash-chain journal and verifier early, before advanced Merkle mirrors.

Human moderation workload:

- Mitigation: build operator tools before adding high-volume public intake.

Sortition legitimacy:

- Mitigation: publish pool hash, ruleset hash, seed bundle, draw code version, and replay transcript for every run.

Privacy leakage:

- Mitigation: separate identity vault from civic projections, minimize public metadata, and avoid raw PII in journal records.

AI misuse:

- Mitigation: keep AI outputs draft-only and require human review for public or official use.

Scope creep:

- Mitigation: keep mobile apps, Telegram, federation, full media automation, and advanced cryptography out of the MVP.

## Governance and Documentation Work

Add these documents before a public pilot:

- `docs/adr/0001-stack.md`
- `docs/adr/0002-journal-first.md`
- `docs/adr/0003-identity-separation.md`
- `docs/adr/0004-ukrainian-canonical-language.md`
- `docs/operations/moderation-runbook.md`
- `docs/operations/correspondence-runbook.md`
- `docs/operations/sortition-runbook.md`
- `docs/operations/incident-response.md`
- `docs/security/threat-model.md`
- `docs/security/disclosure-policy.md`
- `docs/api/public-api.md`

## Success Metrics

Product:

- verified members as percent of registered members
- proposal approval and merge rates
- median moderation time
- mandate invitation acceptance rate
- panel no-show rate
- median time from proposal to panel decision
- median time from resolution to official correspondence
- percent of correspondence overdue
- percent of resolutions with official response

Trust:

- percent of authoritative events journaled
- journal verification success rate
- public checkpoint publication delay
- sortition replay success rate
- number of unresolved audit inconsistencies

Safety:

- harassment incident rate
- moderation appeal rate
- privacy incident count
- policy violation count by mandate holders

Operations:

- API uptime
- public portal latency
- queue depth
- backup restore success
- release rollback success

## Final Recommendation

Start with a modular monolith and a small number of well-defined supporting services. Build the trust spine first: identity separation, journaled state transitions, proposal graph, reproducible sortition, mandate lifecycle, resolution publication, and correspondence tracking.

The first implementation should feel operationally boring and procedurally serious. Viche's legitimacy will come from reproducible process, lawful limits, public memory, and disciplined civic workflow, not from a flashy interface or premature infrastructure complexity.
