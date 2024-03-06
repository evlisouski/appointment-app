from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import parse_obj_as

from app.providers.dao import ProviderDAO
from app.providers.schemas import SNewProvider, SProvider
from app.users.models import User
from app.users.dependencies import get_current_user
from app.exceptions import UserIsNotPresentException
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/providerers",
    tags=["Providers"],
)

@router.get("/all")
@cache(expire=3)
async def get_providers() -> list[SProvider]:
    return await ProviderDAO.get_providers()

@router.get("/user_providers")
async def get_user_providers(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise UserIsNotPresentException
    user_id = current_user.id
    print(user_id)
    return await ProviderDAO.get_providers(user_id=user_id)


@router.get("/{provider_id}")
async def get_provider_by_id(provider_id: int) -> SProvider:
    return await ProviderDAO.get_provider_by_id(provider_id=provider_id)

@router.post("/add")
async def add_provider(provider: SNewProvider, current_user: User = Depends(get_current_user)):
    values = {k: v for k, v in (provider.model_dump()).items() if v is not None}
    values["user_id"] = current_user.id
    return await ProviderDAO.add_provider(**values)

@router.delete("/{provider_id}")
async def del_provider(provider_id: int):
    await ProviderDAO.del_provider(provider_id=provider_id)
