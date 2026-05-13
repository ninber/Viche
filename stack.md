**Custom API-first backend + proven open-source infrastructure + optional integrations with existing civic tools.**

## Recommended core stack

### Backend

Use **Python + FastAPI** or **TypeScript + NestJS**.

My preference: **Python + FastAPI** for the first serious version, because Viche will need a lot of AI-assisted summarization, text classification, multilingual processing, moderation support, and data pipelines. Python will be easier for that.

Use:

* **FastAPI** for the public API and internal services.
* **Pydantic** for strict schemas.
* **SQLAlchemy 2.0 / SQLModel** for database models.
* **Alembic** for migrations.
* **Celery / Dramatiq / RQ** for background jobs.

TypeScript/NestJS is also good, especially for enterprise-style structure, but Python will be more flexible for AI and deliberation analytics.

### Database

Use **PostgreSQL** as the main database.

This is the boring correct choice. Viche will need relational integrity, permissions, jurisdiction trees, mandates, sessions, issue graphs, official correspondence, audit projections, and reporting. PostgreSQL also has logical replication, row-level security, full-text search, JSONB, and strong operational maturity. PostgreSQL logical replication is explicitly designed for replicating selected data changes and supports fine-grained replication/security models. ([PostgreSQL][1])

Use:

* **PostgreSQL** for source-of-truth projections.
* **pgvector** later for semantic duplicate detection.
* **PostGIS** later if geographic/jurisdiction mapping becomes important.
* **Redis** for queues, cache, rate limits, session hints.

### Immutable journal layer

Do **not** rely on ordinary database audit tables.

Create a separate **Journal Service**:

* append-only hash-chained records;
* canonical JSON payloads;
* per-record signatures;
* Merkle checkpoints;
* external mirrors;
* public verifier.

For the public transparency layer, use ideas/tools from **Sigstore Rekor**, **Trillian-style transparency logs**, or a custom minimal transparency log. Rekor is designed as an immutable, tamper-resistant ledger for signed metadata, and supports inclusion/integrity verification through a REST API and CLI. ([Sigstore][2])

For Viche MVP, I would do:

1. Custom journal service in Python/Go/Rust.
2. Store raw journal records in PostgreSQL + object storage.
3. Publish periodic checkpoints to external mirrors.
4. Later integrate Rekor/Trillian-style verification.

Do not start with cryptocurrency blockchain. It adds complexity, politics, cost, and dependency without solving the main problem better than transparency logs.

### Frontend

Use **Next.js + React + TypeScript**.

This is the best general-purpose choice for:

* public website;
* member dashboard;
* mandate console;
* chamber pages;
* resolution tracker;
* multilingual UI;
* admin/moderator panels.

Use:

* **Next.js**
* **React**
* **TypeScript**
* **Tailwind CSS**
* **shadcn/ui**
* **TanStack Query**
* **Zod**
* **i18next / Lingui / FormatJS** for localization.

For mobile later:

* **React Native / Expo**, if you want fast cross-platform mobile apps.
* But MVP should be web-first and responsive.

### Identity and access

Use **Keycloak** as the identity broker.

Keycloak is a mature open-source identity provider and supports OpenID Connect flows. This lets Viche avoid writing its own login/security system from scratch. ([PostgreSQL][3])

Use:

* **Keycloak** for OIDC/OAuth2.
* **WebAuthn / passkeys** for strong authentication.
* National identity adapters per country: Diia.Signature / BankID for Ukraine, eIDAS/EUDI for EU, etc.
* Separate **Identity Vault** from public civic identity.

Very important design rule:

> Legal identity and civic activity must be separated.

The system may need to know that a person is real and eligible, but public deliberation should normally use pseudonymous mandate identities.

### Authorization and policy rules

Use **Open Policy Agent (OPA)** for policy-as-code.

Viche will have many rules:

* who can vote;
* who can moderate;
* who can see sealed data;
* who can publish resolutions;
* when mandate access expires;
* what mandate holders are forbidden to do;
* non-electioneering restrictions;
* jurisdiction-based permissions.

OPA is designed as a general-purpose policy engine for authorization and policy enforcement. ([wiki.postgresql.org][4])

Recommended:

* app-level RBAC/ABAC in backend;
* OPA for high-level policy decisions;
* all policy versions stored in the immutable journal.

### Search and duplicate detection

Start simple:

* PostgreSQL full-text search;
* trigram similarity;
* tags;
* jurisdiction filtering.

Then add:

* **OpenSearch** or **Meilisearch** for public search;
* **pgvector** for semantic similarity;
* AI-assisted duplicate/alternative detection.

For MVP, I would avoid Elastic/OpenSearch unless needed. PostgreSQL + pgvector can go surprisingly far.

### Real-time events

Use:

* **Server-Sent Events** for simple public live updates.
* **WebSockets** only where needed.
* **NATS** or **Redpanda/Kafka** later for internal event streaming.

For MVP:

> PostgreSQL + background workers + outbox pattern is enough.

Do not start with Kafka unless you already have national-scale traffic. PostgreSQL logical replication and event/outbox patterns are easier to operate early.

### Video and deliberation sessions

Use **Jitsi Meet** for self-hosted video.

Jitsi is open-source, self-hostable, and has official self-hosting documentation. Its docs note that HTTPS and proper certificates are important, especially for mobile clients. ([jitsi.github.io][5])

Architecture:

* Jitsi for live chamber sessions.
* Stream to YouTube/Twitch/etc. when public.
* Store metadata, links, transcripts, agenda, questions in Viche.
* Do not store huge video archives in the main database.

For transcription:

* Whisper / faster-whisper for MVP.
* Later: country-specific ASR models.

### Civic participation integrations

Do not make Decidim or Polis the core, but study/reuse patterns.

**Decidim** is a mature participatory democracy platform created initially by Barcelona City Hall, with modules for participatory processes, assemblies, proposals, accountability, and a GraphQL API. ([docs.decidim.org][6])

**Polis** is useful for large-scale opinion mapping; it is open-source and designed for gathering and analyzing large-scale open-ended feedback. ([GitHub][7])

Best approach:

* Viche core: custom.
* Decidim ideas: proposals, accountability, participatory processes.
* Polis integration: mass sentiment/opinion clustering.
* Loomio-like patterns: small group decisions.

### DevOps

For MVP:

* **Docker Compose**
* **PostgreSQL**
* **Redis**
* **MinIO**
* **Keycloak**
* **FastAPI services**
* **Next.js frontend**
* **Jitsi optional/separate**

For serious deployment:

* **Kubernetes** or **Nomad**
* **PostgreSQL managed or Patroni cluster**
* **S3-compatible storage**
* **Prometheus + Grafana**
* **Loki / OpenTelemetry**
* **GitHub Actions / GitLab CI**
* **Terraform / OpenTofu**
* **Ansible** for simpler deployments.

### Supply-chain security

Use:

* **Sigstore/cosign** for signing builds/containers.
* **SLSA-style provenance** later.
* **Dependabot/Renovate**.
* **SBOM generation**.
* **Rekor or self-hosted transparency log** for release metadata.

This matters because Viche’s legitimacy depends not only on civic rules, but also on people being able to verify that software releases were not silently altered.

## Best MVP stack

For the first real implementation, I would choose this:

```text
Frontend:
Next.js + React + TypeScript + Tailwind + shadcn/ui

Backend:
Python + FastAPI + Pydantic + SQLAlchemy + Alembic

Database:
PostgreSQL + Redis

Identity:
Keycloak + OIDC + WebAuthn/passkeys

Policy:
Open Policy Agent

Journal:
Custom append-only hash-chained journal service
+ signed Merkle checkpoints
+ public verifier CLI

Search:
PostgreSQL full-text search first
pgvector later

Video:
Jitsi Meet integration, not deeply embedded at first

Object storage:
MinIO / S3

DevOps:
Docker Compose first
Kubernetes later

Monitoring:
Prometheus + Grafana + OpenTelemetry

AI:
Python workers, model-provider abstraction, human review required
```

## What I would avoid at the start

Avoid these in MVP:

* cryptocurrency blockchain;
* DAO/token mechanics;
* full microservice architecture;
* Kafka from day one;
* mobile app before web MVP;
* fully custom identity system;
* making Telegram the main platform;
* making Decidim the core;
* premature federation between countries.

## Final recommendation

Build Viche as:

> **FastAPI + PostgreSQL + Keycloak + Next.js + custom cryptographic journal.**

That gives you the best balance between:

* speed of development;
* open-source friendliness;
* auditability;
* multilingual expansion;
* strong identity;
* future country packs;
* AI integration;
* realistic deployment in Ukraine, EU, or US contexts.

The most important architectural decision is not the frontend framework. It is this:

> **The immutable journal must be the civic source of truth. Everything else is a projection, interface, or convenience layer.**

[1]: https://www.postgresql.org/docs/current/static/logical-replication.html?utm_source=chatgpt.com "PostgreSQL: Documentation: 18: Chapter 29. Logical Replication"
[2]: https://docs.sigstore.dev/logging/overview/?utm_source=chatgpt.com "Rekor - Sigstore"
[3]: https://www.postgresql.org/docs/16/logical-replication-security.html?utm_source=chatgpt.com "PostgreSQL: Documentation: 16: 31.9. Security"
[4]: https://wiki.postgresql.org/wiki/Row-security?utm_source=chatgpt.com "Row-security - PostgreSQL wiki"
[5]: https://jitsi.github.io/handbook/docs/devops-guide/?utm_source=chatgpt.com "Self-Hosting Guide - Overview | Jitsi Meet"
[6]: https://docs.decidim.org/en/develop/index.html?utm_source=chatgpt.com "Welcome to Decidim Documentation :: Decidim Docs"
[7]: https://github.com/compdemocracy/polis?utm_source=chatgpt.com "GitHub - compdemocracy/polis: :milky_way: Open Source AI for large scale open ended feedback · GitHub"
