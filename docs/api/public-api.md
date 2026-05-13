# Public API

The public API will expose proposals, panels, resolutions, correspondence status, transparency checkpoints, and event feeds without exposing private identity data.

Initial API documentation is generated from the FastAPI OpenAPI schema at `/docs`.

## Implemented Pilot Endpoints

- `POST /v1/members/register` creates a pilot member, public identity, consent record, and journal entry.
- `GET /v1/members/{member_id}` reads a member and public identity.
- `POST /v1/proposals` creates a submitted proposal and journal entry.
- `GET /v1/public/proposals` lists submitted proposals.

The implemented write paths are still pilot-level. They use the journal hash chain and database persistence, but production identity, authorization, moderation, and redaction rules are not complete yet.
