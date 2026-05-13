from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.domain.roadmap import (
    FEDERATION_ARTIFACT_TYPES,
    FEDERATION_RELATIONSHIP_TYPES,
    FederationArtifactType,
    FederationNode,
    FederationRelationshipType,
)

router = APIRouter()


class ArtifactSignature(BaseModel):
    key_id: str
    algorithm: Literal["ed25519"] = "ed25519"
    value: str


class ArtifactEnvelope(BaseModel):
    protocol_version: str = "viche-federation-0.1"
    artifact_type: str
    artifact_id: str
    origin_node_id: str
    origin_journal_entry_id: str
    origin_checkpoint_id: str | None = None
    origin_created_at: datetime
    exported_at: datetime
    export_reason: str
    source_language: str = "uk-UA"
    canonical_payload_hash: str
    redaction_profile: str = "public"
    signature: ArtifactSignature


class ArtifactReceipt(BaseModel):
    status: Literal["received"]
    received_at: datetime
    verification_status: Literal["queued"]


@router.get("/federation/node", response_model=FederationNode)
async def get_node_metadata() -> FederationNode:
    return FederationNode(
        node_id="LOCAL-VICHE",
        name="Local Viche Development Node",
        scope="local-development",
        protocol_versions=["viche-federation-0.1"],
        supported_languages=["uk-UA", "en-US"],
        public_api_base="http://localhost:8000/v1",
        transparency_log_url=None,
    )


@router.get("/federation/relationship-types", response_model=list[FederationRelationshipType])
async def get_relationship_types() -> list[FederationRelationshipType]:
    return FEDERATION_RELATIONSHIP_TYPES


@router.get("/federation/artifact-types", response_model=list[FederationArtifactType])
async def get_artifact_types() -> list[FederationArtifactType]:
    return FEDERATION_ARTIFACT_TYPES


@router.post(
    "/federation/inbox/artifacts",
    response_model=ArtifactReceipt,
    status_code=status.HTTP_202_ACCEPTED,
)
async def receive_artifact(envelope: ArtifactEnvelope) -> ArtifactReceipt:
    return ArtifactReceipt(
        status="received",
        received_at=datetime.now(UTC),
        verification_status="queued",
    )

