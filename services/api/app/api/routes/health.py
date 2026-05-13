from typing import Literal

import redis.asyncio as redis
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine

router = APIRouter()


class ComponentStatus(BaseModel):
    status: Literal["ok", "error"]
    detail: str | None = None


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    service: str
    environment: str
    database: ComponentStatus
    redis: ComponentStatus


async def _check_database() -> ComponentStatus:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("select 1"))
        return ComponentStatus(status="ok")
    except Exception as exc:
        return ComponentStatus(status="error", detail=exc.__class__.__name__)


async def _check_redis() -> ComponentStatus:
    client = redis.from_url(settings.redis_url)
    try:
        await client.ping()
        return ComponentStatus(status="ok")
    except Exception as exc:
        return ComponentStatus(status="error", detail=exc.__class__.__name__)
    finally:
        await client.aclose()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    database = await _check_database()
    redis_status = await _check_redis()
    status: Literal["ok", "degraded"] = (
        "ok" if database.status == "ok" and redis_status.status == "ok" else "degraded"
    )

    return HealthResponse(
        status=status,
        service="viche-api",
        environment=settings.app_env,
        database=database,
        redis=redis_status,
    )

