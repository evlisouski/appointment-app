from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.customers.dao import CustomerDAO
from app.customers.schemas import SCustomer, SNewCustomer, SNewCustomerReturn

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get("/{id}")
async def get_customer_by_id(id: int) -> SCustomer:
    return await CustomerDAO.get_customer_by_id(customer_id=id)


@router.get("/all")
async def get_customers() -> list[SCustomer]:
    return await CustomerDAO.get_customers()


@router.post("/add")
async def add_customer(customer: SNewCustomer) -> SNewCustomerReturn:
    return await CustomerDAO.add_customer(
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
