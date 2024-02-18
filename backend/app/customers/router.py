from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.customers.dao import CustomerDAO
from app.customers.schemas import SCustomer, SNewCustomer, SNewCustomerReturn
from app.users.dependencies import get_current_user
from app.users.models import User
from app.exceptions import UserAlreadyExistsException

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

@router.get("/all")
async def get_customers() -> list[SCustomer]:
    return await CustomerDAO.find_all()

@router.get("/customer{id}")
async def get_customer_by_id(id: int) -> SCustomer | None:
    return await CustomerDAO.find_one_or_none(id=id)


@router.post("/add")
async def add_customer(customer: SNewCustomer, current_user: User = Depends(get_current_user)) -> SNewCustomerReturn:
    is_user = await CustomerDAO.find_one_or_none(id=current_user.id)
    if is_user:
        raise UserAlreadyExistsException
    # print(await get_current_user())
    return await CustomerDAO.add_customer(
        id=current_user.id,
        name=customer.name,
        birthday=customer.birthday,
        registration_date=customer.registration_date,
        rating=customer.rating,
        verified=customer.verified,
        location=customer.location,
        image_id=customer.image_id,
        score=customer.score,
    )

@router.delete("/{customer_id}")
async def remove_booking(customer_id: int):
    await CustomerDAO.delete(id=customer_id)
