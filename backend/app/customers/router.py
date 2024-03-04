from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.customers.dao import CustomerDAO
from app.customers.schemas import SCustomer, SNewCustomer, SNewCustomerReturn
from app.users.dependencies import get_current_user
from app.users.models import User
from app.exceptions import AccessDenied, UserAlreadyExistsException
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

@router.get("/all")
@cache(expire=3)
async def get_customers() -> list[SCustomer]:    
    return await CustomerDAO.find_all()

@router.get("/customer{id}")
async def get_customer_by_id(id: int) -> SCustomer | None:
    return await CustomerDAO.find_one_or_none(id=id)

@router.post("/add")
async def add_customer(customer: SNewCustomer,
                       current_user: User = Depends(get_current_user)) -> SNewCustomerReturn:
    is_user = await CustomerDAO.find_one_or_none(id=current_user.id)
    if is_user:
        raise UserAlreadyExistsException    
    values = {k: v for k, v in (customer.model_dump()).items() if v is not None}
    values["id"] = current_user.id
    return await CustomerDAO.add_customer(**values)

@router.delete("/{customer_id}")
async def remove_booking(customer_id: int,
                         current_user: User = Depends(get_current_user)):
    if await CustomerDAO.find_one_or_none(id=current_user.id):
        raise AccessDenied
    await CustomerDAO.delete(id=customer_id)
