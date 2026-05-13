from typing import Literal

from pydantic import BaseModel

ModuleStatus = Literal["planned", "skeleton", "pilot", "production"]
ModuleLayer = Literal["trust", "civic", "interaction", "federation"]


class SystemModule(BaseModel):
    key: str
    name: str
    layer: ModuleLayer
    status: ModuleStatus
    purpose: str
    plan_reference: str


class FederationNode(BaseModel):
    node_id: str
    name: str
    scope: str
    protocol_versions: list[str]
    supported_languages: list[str]
    public_api_base: str
    transparency_log_url: str | None = None


class FederationRelationshipType(BaseModel):
    key: str
    direction: Literal["up", "down", "peer", "mirror", "partner"]
    purpose: str


class FederationArtifactType(BaseModel):
    key: str
    can_travel_up: bool
    can_travel_down: bool
    can_travel_peer: bool
    contains_private_data_by_default: bool


PLAN_1_MODULES: list[SystemModule] = [
    SystemModule(
        key="membership",
        name="Membership and identity separation",
        layer="trust",
        status="pilot",
        purpose="Stable members, assurance levels, consent records, and public-safe identities.",
        plan_reference="Plan_1.md Phase 1",
    ),
    SystemModule(
        key="journal",
        name="Tamper-evident journal",
        layer="trust",
        status="pilot",
        purpose="Hash-chained civic event log, checkpoints, and verifier exports.",
        plan_reference="Plan_1.md Phase 2",
    ),
    SystemModule(
        key="proposals",
        name="Issue and proposal graph",
        layer="civic",
        status="pilot",
        purpose="Proposal intake, moderation, evidence, duplicates, alternatives, and relations.",
        plan_reference="Plan_1.md Phase 3",
    ),
    SystemModule(
        key="sortition",
        name="Sortition and mandates",
        layer="trust",
        status="skeleton",
        purpose="Eligible pool snapshots, reproducible draws, invitations, mandates, and COI.",
        plan_reference="Plan_1.md Phase 4",
    ),
    SystemModule(
        key="panels",
        name="Panels and deliberation",
        layer="civic",
        status="skeleton",
        purpose="Panel lifecycle, agendas, evidence packs, sessions, and transcripts.",
        plan_reference="Plan_1.md Phase 5",
    ),
    SystemModule(
        key="resolutions",
        name="Resolutions and votes",
        layer="civic",
        status="skeleton",
        purpose="Draft resolutions, votes, minority notes, publication, and redaction.",
        plan_reference="Plan_1.md Phase 5",
    ),
    SystemModule(
        key="correspondence",
        name="Official correspondence and follow-up",
        layer="civic",
        status="skeleton",
        purpose="Dispatch, delivery confidence, official responses, deadlines, and escalation.",
        plan_reference="Plan_1.md Phase 6",
    ),
    SystemModule(
        key="notifications",
        name="Notifications and event feeds",
        layer="interaction",
        status="skeleton",
        purpose="In-app notices, acknowledgements, signed webhooks, and public streams.",
        plan_reference="Plan_1.md Phase 7",
    ),
    SystemModule(
        key="federation",
        name="Hierarchical federation",
        layer="federation",
        status="skeleton",
        purpose="Signed proposal, resolution, evidence, and correspondence flow across nodes.",
        plan_reference="Plan_2.md",
    ),
]


FEDERATION_RELATIONSHIP_TYPES: list[FederationRelationshipType] = [
    FederationRelationshipType(
        key="parent_of",
        direction="down",
        purpose="Higher-level node contains lower-level civic scope.",
    ),
    FederationRelationshipType(
        key="child_of",
        direction="up",
        purpose="Lower-level node belongs under a higher-level civic scope.",
    ),
    FederationRelationshipType(
        key="peer_of",
        direction="peer",
        purpose="Similar-level nodes share proposals, alternatives, evidence, or joint requests.",
    ),
    FederationRelationshipType(
        key="partner_of",
        direction="partner",
        purpose="Trusted non-hierarchical civic partner relationship.",
    ),
    FederationRelationshipType(
        key="mirror_of",
        direction="mirror",
        purpose="Read-only public transparency mirror relationship.",
    ),
]


FEDERATION_ARTIFACT_TYPES: list[FederationArtifactType] = [
    FederationArtifactType(
        key="proposal",
        can_travel_up=True,
        can_travel_down=True,
        can_travel_peer=True,
        contains_private_data_by_default=False,
    ),
    FederationArtifactType(
        key="evidence_bundle",
        can_travel_up=True,
        can_travel_down=True,
        can_travel_peer=True,
        contains_private_data_by_default=False,
    ),
    FederationArtifactType(
        key="panel_resolution",
        can_travel_up=True,
        can_travel_down=True,
        can_travel_peer=True,
        contains_private_data_by_default=False,
    ),
    FederationArtifactType(
        key="correspondence_status",
        can_travel_up=True,
        can_travel_down=True,
        can_travel_peer=False,
        contains_private_data_by_default=False,
    ),
    FederationArtifactType(
        key="transparency_checkpoint",
        can_travel_up=True,
        can_travel_down=True,
        can_travel_peer=True,
        contains_private_data_by_default=False,
    ),
]
