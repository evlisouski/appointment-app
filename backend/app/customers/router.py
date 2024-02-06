from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.customers.dao import CustomerDAO
from app.customers.schemas import SCustomer

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get("")
async def get_customers() -> list[SCustomer]:
    return await CustomerDAO.find_all()
