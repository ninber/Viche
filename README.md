# Viche

Viche is a civic deliberation platform project for lawful, structured public participation. The project aims to organize civic signals, proposals, evidence, rotating deliberative panels, public recommendations, official correspondence, and transparent follow-up without becoming a political party, campaign tool, or substitute for public institutions.

The repository is currently documentation-first. The technical direction is described in:

- `TechnicalTask.md`
- `Architecture.md`

## Core Direction

Viche should be built as API-first civic infrastructure with:

- Ukrainian as the canonical domain language.
- Versioned multilingual documents and translations.
- Progressive identity assurance for different trust levels.
- Sortition, rotation, and temporary civic mandates.
- Structured proposal and evidence graphs.
- Append-only audit logs and public transparency checkpoints.
- Official correspondence tracking and public follow-up.
- AI-assisted search, deduplication, summarization, and translation support, but not AI-made civic decisions.

## Documents

Some root documents have language counterparts:

- `Маніфест Віче.md` and `The Viche Manifesto.md`
- `Протокол мандата Віче.md` and `Viche Mandate Protocol.md`

When documents differ, treat the Ukrainian version as authoritative unless a file explicitly says otherwise.

## Development Skeleton

The initial project skeleton follows `Plan_1.md`:

- `apps/web` - Next.js public portal/member/operator UI shell.
- `services/api` - FastAPI backend shell with `/v1/health`.
- `packages/schemas` - shared JSON Schema contracts.
- `packages/policy` - initial OPA policy bundle.
- `packages/verifier` - journal verifier CLI skeleton.
- `infra/compose` - local PostgreSQL, Redis, MinIO, Keycloak, API, and web stack.

Start the local stack:

```bash
docker compose up --build
```

Useful local URLs:

- Web: `http://localhost:3000`
- API health: `http://localhost:8000/v1/health`
- API docs: `http://localhost:8000/docs`
- Keycloak: `http://localhost:8080`
- MinIO console: `http://localhost:9001`

## License

This project is licensed under the GNU Affero General Public License v3.0 only.

SPDX-License-Identifier: AGPL-3.0-only

See `LICENSE` for the full license text.
