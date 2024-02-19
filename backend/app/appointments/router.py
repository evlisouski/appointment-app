from fastapi import APIRouter, Depends
from app.appointments.dao import AppointmentDAO
from app.appointments.schemas import SAppointment
from app.appointments.dependencies import get_current_provider
from app.appointments.models import Appointment
from app.exceptions import UserIsNotPresentException

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

@router.post("/add")
async def add_appointment(appointment: SAppointment, current_provider: Appointment = Depends(get_current_provider)):
    if not current_provider:
        raise UserIsNotPresentException
    provider_ids = [i["id"] for i in current_provider]
    if appointment.provider_id not in provider_ids:
        raise UserIsNotPresentException
    return await AppointmentDAO.add_appointment(        
        provider_id=appointment.provider_id,
        customer_id=appointment.customer_id,
        offer=appointment.offer,
        datetime_from=appointment.datetime_from,
        datetime_to=appointment.datetime_to,
        price=appointment.price
    )
