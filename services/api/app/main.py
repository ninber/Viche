from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.federation import router as federation_router
from app.api.routes.health import router as health_router
from app.api.routes.members import router as members_router
from app.api.routes.proposals import router as proposals_router
from app.api.routes.public import router as public_router
from app.api.routes.sortition import router as sortition_router
from app.api.routes.system import router as system_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Viche API",
        version="0.1.0",
        description="API-first civic deliberation platform skeleton.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix="/v1", tags=["health"])
    app.include_router(system_router, prefix="/v1", tags=["system"])
    app.include_router(members_router, prefix="/v1", tags=["members"])
    app.include_router(proposals_router, prefix="/v1", tags=["proposals"])
    app.include_router(sortition_router, prefix="/v1", tags=["sortition"])
    app.include_router(public_router, prefix="/v1", tags=["public"])
    app.include_router(federation_router, prefix="/v1", tags=["federation"])
    return app


app = create_app()
