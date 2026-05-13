from fastapi import APIRouter
from pydantic import BaseModel

from app.domain.roadmap import PLAN_1_MODULES, SystemModule

router = APIRouter()


class SystemOverview(BaseModel):
    name: str
    canonical_language: str
    modules: list[SystemModule]


@router.get("/system", response_model=SystemOverview)
async def get_system_overview() -> SystemOverview:
    return SystemOverview(
        name="Viche",
        canonical_language="uk-UA",
        modules=PLAN_1_MODULES,
    )

