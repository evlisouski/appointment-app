from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import parse_obj_as

from app.providers.dao import ProviderDAO
from app.providers.schemas import SProvider


router = APIRouter(
    prefix="/providerers",
    tags=["Providers"],
)

@router.get("/all")
async def get_providers() -> list[SProvider]:
    return await ProviderDAO.get_providers()

@router.get("/{id}")
async def get_provider_by_id(id: int):
    return await ProviderDAO.get_provider_by_id(provider_id=id)