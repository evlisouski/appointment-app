from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import parse_obj_as

from app.providers.dao import ProviderDAO


router = APIRouter(
    prefix="/providerers",
    tags=["Providers"],
)


@router.get("")
async def get_providers(provider_id: int):
    return await ProviderDAO.get_provider_by_id(provider_id=provider_id)
