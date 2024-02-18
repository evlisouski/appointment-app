from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import parse_obj_as

from app.providers.dao import ProviderDAO
from app.providers.schemas import SNewProvider, SProvider
from app.users.models import User
from app.users.dependencies import get_current_user
from app.exceptions import UserAlreadyExistsException


router = APIRouter(
    prefix="/providerers",
    tags=["Providers"],
)

@router.post("/add")
async def add_provider(provider: SNewProvider, current_user: User = Depends(get_current_user)):
    return await ProviderDAO.add_provider(
        user_id=current_user.id,
        name=provider.name,
        foundation_date=provider.foundation_date,
        registration_date=provider.registration_date,
        rating=provider.rating,
        verified=provider.verified,
        location=provider.location,
        image_id=provider.image_id,
        tags=provider.tags,
    )

@router.get("/all")
async def get_providers() -> list[SProvider]:
    return await ProviderDAO.get_providers()


@router.get("/{id}")
async def get_provider_by_id(id: int) -> SProvider:
    return await ProviderDAO.get_provider_by_id(provider_id=id)


@router.delete("/{provider_id}")
async def del_provider(provider_id: int):
    await ProviderDAO.del_provider(provider_id=provider_id)
