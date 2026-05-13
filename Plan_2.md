# Viche Plan 2: Hierarchical Interoperability and Proposal Flow

## Purpose

This plan describes how one Viche instance can connect to another Viche-like system at a lower, higher, or peer level. Examples:

- town or community instance -> district instance
- district instance -> regional instance
- regional instance -> national instance
- national instance -> regional or town instances
- one civic organization instance -> another compatible civic organization instance

The goal is bidirectional travel of proposals, evidence, resolutions, correspondence status, and public accountability signals while preserving local autonomy, provenance, privacy, and auditability.

This is not first-MVP functionality. It should be designed early in the domain model, but implemented after the local pilot proves identity, proposal graph, sortition, resolution, journal, and correspondence workflows.

## Core Principle

Viche should federate civic artifacts, not control people across instances.

A higher-level node must not silently take over a lower-level node. A lower-level node must not be able to forge national legitimacy. Each node remains sovereign over its own membership, moderation, panels, resolutions, correspondence, and journal. Cross-level flow happens through signed referrals, imports, endorsements, adoptions, escalations, and responses.

## Network Model

Each Viche deployment is a `node`.

Node examples:

- `UA-NATIONAL`
- `UA-REGION-KYIV-OBLAST`
- `UA-CITY-KYIV`
- `UA-TOWN-BUCHA`
- `UA-DISTRICT-PECHERSK`
- `NGO-PARTNER-EXAMPLE`

Each node has:

- stable node ID
- public name
- jurisdiction or organizational scope
- public API base URL
- public key set
- supported protocol versions
- supported languages
- accepted trust levels
- public transparency log URL
- moderation/contact channel
- parent node, child nodes, and peer links where applicable

## Relationship Types

Use explicit relationships instead of assuming one global hierarchy.

| Relationship | Meaning | Example |
|---|---|---|
| `parent_of` | Higher-level civic scope contains lower-level scope | national node is parent of regional node |
| `child_of` | Lower-level civic scope belongs under higher-level scope | town node is child of region node |
| `peer_of` | Similar-level cooperation | two city nodes share transport issue data |
| `observer_of` | One node can monitor public artifacts but not import automatically | university research mirror observes public logs |
| `partner_of` | Non-hierarchical trusted NGO/civic partner | partner NGO sends evidence bundles |
| `mirror_of` | Read-only transparency mirror | archive node mirrors checkpoints |

Relationships must be policy-controlled and journaled by both sides.

## Artifact Types That Can Travel

Initial supported artifact types:

- proposal
- proposal relation
- issue cluster
- evidence bundle
- moderation label
- panel resolution
- minority note
- correspondence record
- official response
- deadline/escalation status
- transparency checkpoint
- public analytics aggregate

Do not exchange raw private identity records, sealed deliberation materials, private moderator notes, or unredacted personal data by default.

## Flow Directions

### Upward Flow

Lower-level nodes can send artifacts upward when a problem exceeds local scope.

Examples:

- A town submits a proposal to a regional node because the issue concerns oblast infrastructure.
- Several city nodes escalate similar hospital access complaints to a regional health panel.
- A regional node forwards a resolution to the national node because it requires ministry action.

Upward flow types:

- `refer_up`
- `escalate_up`
- `request_review_up`
- `aggregate_up`
- `petition_up`
- `publish_for_parent_awareness`

### Downward Flow

Higher-level nodes can send artifacts downward for local review, implementation, consultation, or follow-up.

Examples:

- A national resolution asks regional nodes to collect evidence about implementation.
- A regional node sends a transport proposal to affected towns for local comment.
- A national node publishes a model recommendation that local nodes may adopt or reject.

Downward flow types:

- `request_local_review`
- `request_evidence`
- `request_vote_or_deliberation`
- `delegate_followup`
- `publish_model_resolution`
- `send_guidance`

### Peer Flow

Nodes at similar level can share artifacts horizontally.

Examples:

- Two towns share duplicate water-service proposals.
- Cities compare alternative transport policies.
- Regional nodes share evidence on a national procurement issue.

Peer flow types:

- `share_duplicate_candidate`
- `share_alternative`
- `share_evidence`
- `request_joint_panel`
- `request_co_signature`

## Artifact Lifecycle Across Nodes

An imported artifact must never overwrite the local artifact directly. It becomes a local `external_artifact` record first.

Recommended lifecycle:

```text
received -> verified -> triaged -> linked -> accepted | rejected | needs_more_info
accepted -> localized -> mapped_to_local_scope -> deliberated | adopted | escalated | archived
```

For outgoing artifacts:

```text
draft_export -> policy_checked -> redacted -> signed -> sent -> received_ack -> imported_by_remote | rejected_by_remote | expired
```

## Cross-Node Actions

Use precise action names so public observers understand what happened.

| Action | Description |
|---|---|
| `imported` | Node stores a remote artifact as external input |
| `linked` | Node relates a local artifact to a remote artifact |
| `endorsed` | Node agrees with a remote artifact but does not make it its own |
| `adopted` | Node turns remote artifact into a local official artifact |
| `adapted` | Node creates a modified local version based on a remote artifact |
| `escalated` | Node sends local artifact to a higher-level node |
| `delegated` | Node asks a lower-level node to handle follow-up |
| `rejected` | Node declines import/adoption and records reason |
| `superseded` | Node marks a local copy as replaced by a newer version |
| `withdrawn` | Origin node withdraws the artifact, without deleting receiving nodes' audit history |

## Identity and Privacy Rules

Cross-node interoperability must not require sharing legal identity by default.

Rules:

1. A sending node should export public-safe civic artifacts only.
2. A receiving node should treat remote member identifiers as foreign pseudonymous actors.
3. Legal identity assertions remain at the origin node unless a specific legal workflow requires explicit transfer.
4. Cross-node panel service requires local eligibility rules. A national node cannot assume a town member is nationally eligible without an eligibility assertion.
5. If an artifact contains personal data, it must carry a redaction profile and purpose limitation.
6. Imported artifacts must preserve origin provenance even after translation or adaptation.

## Provenance Model

Every traveling artifact needs a provenance envelope.

Minimum fields:

```json
{
  "protocol_version": "viche-federation-0.1",
  "artifact_type": "proposal",
  "artifact_id": "origin-local-id",
  "origin_node_id": "UA-TOWN-BUCHA",
  "origin_journal_entry_id": "journal-entry-id",
  "origin_checkpoint_id": "checkpoint-id",
  "origin_created_at": "2026-05-13T00:00:00Z",
  "exported_at": "2026-05-13T00:00:00Z",
  "export_reason": "escalate_up",
  "source_language": "uk-UA",
  "canonical_payload_hash": "sha256:...",
  "redaction_profile": "public",
  "signature": {
    "key_id": "node-key-2026-01",
    "algorithm": "ed25519",
    "value": "..."
  }
}
```

Payloads should be canonical JSON with stable hashing. Large evidence files should travel as manifests with content hashes and object URLs, not as opaque database dumps.

## Trust and Verification

A receiving node must verify:

- origin node is known or explicitly allowed
- artifact signature is valid
- origin key is valid for the export time
- payload hash matches the envelope
- origin checkpoint can be checked or queued for later verification
- redaction profile is compatible with local policy
- artifact type is allowed for that relationship
- requested action is allowed by local policy

Trust is not binary. Suggested trust states:

- `untrusted`
- `known_public`
- `verified_node`
- `partner_node`
- `parent_node`
- `child_node`
- `mirror_node`

Even a parent node should not bypass local moderation and policy checks.

## Conflict and Duplication Handling

Cross-node flow will create duplicates. That is expected.

Local relation types should include:

- `remote_duplicate_of`
- `remote_near_duplicate_of`
- `remote_alternative_to`
- `remote_supports`
- `remote_conflicts_with`
- `remote_escalation_of`
- `remote_delegation_of`
- `remote_adoption_of`
- `remote_adaptation_of`

If two nodes disagree, preserve disagreement explicitly. Do not force a merge.

Conflict examples:

- Town resolution supports road closure; city resolution opposes it.
- Regional node modifies a town proposal before escalating it nationally.
- National node rejects local escalation as outside national scope.

Each conflict should have public-safe rationale and journal entries.

## Proposal Travel Patterns

### Local Proposal Escalated Upward

1. Member submits proposal in town node.
2. Town moderators approve and classify it.
3. Town node detects issue exceeds town competence.
4. Operator creates `escalate_up` export to regional node.
5. Regional node verifies envelope.
6. Regional node imports as `external_artifact`.
7. Regional moderators triage.
8. Regional node links it to local proposal graph.
9. Regional node adopts, adapts, rejects, or aggregates it.
10. Both nodes journal the full chain.

### National Proposal Sent Downward

1. National node publishes proposal or model resolution.
2. National node sends `request_local_review` to affected child nodes.
3. Local nodes import it as external artifact.
4. Local nodes run local deliberation or evidence collection.
5. Local nodes send responses upward.
6. National node aggregates responses and publishes follow-up.

### Similar Local Proposals Aggregated Upward

1. Multiple town nodes publish similar proposals.
2. Regional node receives duplicate candidates.
3. Regional moderator creates issue cluster.
4. Regional panel deliberates at regional scope.
5. Regional resolution links to all source proposals.
6. Town nodes display regional outcome as related follow-up.

## Resolution Travel Patterns

### Resolution Endorsement

A node may endorse a remote resolution without adopting it as its own.

Use when:

- content is aligned
- no local legal signature is required
- public support is useful

Journal event:

- `remote_resolution.endorsed`

### Resolution Adoption

A node may adopt a remote resolution into local authority.

Use when:

- local panel or authorized body approves it
- local signatures are attached
- local correspondence or follow-up will be created

Journal events:

- `remote_resolution.imported`
- `resolution.adopted_from_remote`
- `resolution.published`

### Resolution Adaptation

A node may adapt a remote resolution.

Use when:

- jurisdiction differs
- local law or facts require changes
- translation needs authoritative local review

Journal events:

- `remote_resolution.imported`
- `resolution.adapted_from_remote`
- `resolution.published`

The local resolution must link to the source and explain material changes.

## Correspondence Travel

Correspondence status can also move across levels.

Examples:

- Town sends request to local office and shares unanswered status with regional node.
- Regional node escalates overdue local responses to national dashboard.
- National node delegates ministry response tracking to regional nodes.

Rules:

1. Do not expose private contact details unless policy allows it.
2. Export official replies as redacted records with hashes of originals.
3. Preserve delivery confidence level.
4. Preserve deadline calculations and timezone.
5. Track which node owns the next action.

Ownership states:

- `origin_node_responsible`
- `receiving_node_responsible`
- `joint_followup`
- `waiting_for_official_response`
- `closed_by_origin`
- `closed_by_receiver`

## API Surface

### Node Registry

- `GET /v1/federation/node`
- `GET /v1/federation/relationships`
- `POST /v1/admin/federation/relationships`
- `PATCH /v1/admin/federation/relationships/{id}`

### Artifact Exchange

- `POST /v1/federation/inbox/artifacts`
- `GET /v1/federation/inbox/artifacts`
- `POST /v1/federation/outbox/artifacts`
- `GET /v1/federation/outbox/artifacts/{id}`
- `POST /v1/federation/artifacts/{id}/verify`
- `POST /v1/federation/artifacts/{id}/triage`

### Public Resolution and Proposal Links

- `GET /v1/public/federation/artifacts/{id}`
- `GET /v1/public/proposals/{id}/remote-links`
- `GET /v1/public/resolutions/{id}/remote-links`
- `GET /v1/public/correspondence/{id}/remote-links`

### Event Feeds

Initial webhook/event types:

- `federation.artifact.sent`
- `federation.artifact.received`
- `federation.artifact.verified`
- `federation.artifact.rejected`
- `remote_proposal.imported`
- `remote_proposal.escalated`
- `remote_resolution.imported`
- `remote_resolution.endorsed`
- `remote_resolution.adopted`
- `remote_correspondence.status_updated`

All cross-node webhooks must be signed.

## Data Model Additions

Add these entities after the local MVP stabilizes:

- `federation_node`
- `federation_relationship`
- `federation_key`
- `federation_policy`
- `external_artifact`
- `artifact_envelope`
- `artifact_import`
- `artifact_export`
- `artifact_verification`
- `remote_artifact_link`
- `remote_resolution_action`
- `remote_correspondence_link`
- `federation_delivery_attempt`
- `federation_inbox_event`
- `federation_outbox_event`

Important fields:

- origin node ID
- receiving node ID
- origin artifact type
- origin artifact ID
- local mapped artifact ID
- canonical payload hash
- signature status
- verification status
- import decision
- relationship type
- transfer direction
- redaction profile
- policy version
- journal entry references

## Policy Rules

OPA/federation policy should answer:

- Can this node send this artifact type to that node?
- Can this node receive this artifact type from that node?
- Can this remote artifact be auto-imported, or must it be manually reviewed?
- Can remote content be shown publicly before local moderation?
- Can a remote resolution be endorsed by operators only, or does it require panel approval?
- Can correspondence status be escalated upward?
- Which redaction profile is required?
- Which language/translation state is required?
- Which trust state is required?

No cross-node action should bypass policy evaluation.

## Moderation and Governance

Cross-node import creates a new abuse surface.

Controls:

- allowlist trusted nodes first
- rate limits per remote node
- artifact type limits per relationship
- manual review for public display
- quarantine queue for unknown nodes
- appeal path for rejected imports
- public explanation for rejected official escalations
- emergency pause on a relationship
- public relationship registry

Governance decisions that should be journaled:

- relationship created
- relationship suspended
- remote node key rotated
- federation policy changed
- import rejected for policy reason
- remote artifact adopted or endorsed

## Translation and Localization

Remote artifacts may arrive in different languages.

Rules:

1. Preserve original text.
2. Store machine translation separately.
3. Store human-verified translation separately.
4. Mark which text is authoritative.
5. Do not let translation change the legal or civic meaning without adaptation record.
6. For official local adoption, require local authoritative text in the node's canonical language.

## Transparency and Public Display

Public pages should show:

- source node
- receiving node
- relationship type
- action taken: imported, endorsed, adopted, adapted, rejected, escalated
- artifact provenance
- verification status
- source checkpoint link
- local journal entry link
- material changes if adapted
- local decision rationale

This lets citizens see whether a proposal is originally local, imported from another town, escalated from a region, or delegated by the national node.

## Security Risks

| Risk | Mitigation |
|---|---|
| Remote node sends spam | allowlist, rate limits, quarantine queue |
| Parent node overreaches | local policy gate, public journal, manual acceptance |
| Lower node forges support | signatures, origin verification, membership claims not trusted blindly |
| Personal data leaks across nodes | redaction profiles, PII export bans, purpose limitation |
| Duplicate explosion | remote relation graph, clustering, moderator tools |
| Conflicting resolutions confuse public | explicit conflict relations and public rationale |
| Replay of old artifact | timestamps, nonce/export ID, checkpoint validation |
| Key compromise | key rotation, revocation list, relationship suspension |
| Translation distortion | preserve original, mark translation status, require human review for adoption |

## Implementation Phases

### Phase F0: Design Hooks in Local MVP

Implement now or reserve in schema:

- stable node ID config
- territory/jurisdiction IDs
- proposal and resolution source fields
- journal entry references on public artifacts
- remote link relation types reserved
- public-safe export serializers

Acceptance criteria:

- Local artifacts can be serialized into canonical public-safe JSON.
- Public artifacts carry stable IDs and journal references.

### Phase F1: Read-Only Node Registry and Public Discovery

Implement:

- `GET /v1/federation/node`
- public node metadata
- public key set endpoint
- transparency checkpoint discovery

Acceptance criteria:

- Another node can discover this node's identity, supported protocol version, public keys, and public API base.

### Phase F2: Manual Import and Export

Implement:

- signed export file
- manual upload/import
- signature verification
- moderator triage
- remote artifact links

Acceptance criteria:

- A town node can export a proposal file.
- A regional node can import, verify, link, and accept/reject it.
- Public page shows provenance.

### Phase F3: Federation Inbox and Outbox

Implement:

- authenticated cross-node API
- signed webhooks
- delivery attempts
- retry and expiration
- relationship policy checks

Acceptance criteria:

- Nodes can exchange proposals and resolutions without manual file transfer.
- Failed delivery and rejection are visible to operators.

### Phase F4: Bidirectional Proposal and Resolution Workflows

Implement:

- upward escalation
- downward review request
- peer duplicate sharing
- resolution endorsement
- resolution adoption
- resolution adaptation
- correspondence status sharing

Acceptance criteria:

- A lower node can escalate a proposal upward.
- A higher node can send a resolution downward for local review.
- Local node can adopt or reject remote resolution with journaled rationale.

### Phase F5: Aggregation and Dashboards

Implement:

- regional/national aggregation of related proposals
- cross-node issue clusters
- response deadline dashboards
- unresolved escalation dashboards
- remote artifact analytics

Acceptance criteria:

- Regional or national portal can show how many local nodes raised similar issues.
- Local portal can show what happened after escalation.

### Phase F6: Advanced Interoperability

Only after F1-F5 work:

- shared panel invitations across nodes
- joint panels
- shared evidence repositories
- cross-node verifier tools
- transparency mirrors
- federation SDK
- protocol conformance test suite

## Pilot Scenario

Pilot one town node and one regional node.

Scenario:

1. Town members submit road safety proposals.
2. Town moderators merge duplicates.
3. Town panel publishes a resolution.
4. Town node sends the resolution and evidence bundle to regional node.
5. Regional node verifies the artifact.
6. Regional node links it to similar town proposals.
7. Regional panel adapts it into a regional resolution.
8. Regional node sends follow-up status back down.
9. Town portal shows the regional outcome and correspondence status.
10. Both nodes publish journal entries and checkpoints.

Success means a citizen can trace the chain from local proposal to regional resolution and back to local follow-up without trusting private operator claims.

## Definition of Done

The hierarchical interoperability layer is ready for a controlled pilot when:

- node registry works
- public keys and protocol versions are discoverable
- artifact envelopes are signed and verified
- import/export is journaled
- proposals can escalate upward
- resolutions can be sent downward
- imported artifacts are never silently treated as local originals
- public pages show source, verification, action, and rationale
- policy rules can pause or restrict relationships
- personal data is not exported by default
- verifier tooling can validate exported artifact provenance

## Final Recommendation

Build federation as a protocol layer around signed civic artifacts, not as shared database replication and not as central command. Local, regional, and national Viche nodes should cooperate through transparent, journaled, policy-checked artifact exchange.

This keeps town-level participation meaningful, lets regional and national levels aggregate legitimate local signals, and allows national resolutions to travel downward for real local review instead of becoming one-way announcements.
