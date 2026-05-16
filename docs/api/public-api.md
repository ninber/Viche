# Public API

The public API will expose proposals, panels, resolutions, correspondence status, transparency checkpoints, and event feeds without exposing private identity data.

Initial API documentation is generated from the FastAPI OpenAPI schema at `/docs`.

## Implemented Pilot Endpoints

- `POST /v1/members/register` creates a pilot member, public identity, consent record, and journal entry.
- `GET /v1/members/{member_id}` reads a member and public identity.
- `POST /v1/proposals` creates a submitted proposal and journal entry.
- `PATCH /v1/proposals/{proposal_id}/moderation` changes proposal status and journals the moderation decision.
- `POST /v1/proposals/{proposal_id}/relations` creates a proposal graph edge and journal entry.
- `GET /v1/proposals/{proposal_id}/relations` lists outgoing proposal graph edges.
- `GET /v1/public/proposals` lists submitted proposals.
- `GET /v1/public/resolutions` lists published panel resolutions.
- `POST /v1/eligibility-pools` freezes an active-member eligibility pool and journals the pool hash.
- `POST /v1/sortitions` runs the deterministic pilot sortition algorithm and journals the transcript hash.
- `GET /v1/sortitions/{run_id}` reads a sortition run and selected members.
- `POST /v1/panels` creates a panel from primary sortition results and journals issued mandates.
- `GET /v1/panels/{panel_id}` reads panel mandates and resolutions.
- `POST /v1/panels/{panel_id}/resolutions` drafts or publishes a panel resolution and journals it.

The implemented write paths are still pilot-level. They use the journal hash chain and database persistence, but production identity, authorization, moderation, and redaction rules are not complete yet.
