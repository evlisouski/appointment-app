from typing import Optional
from fastapi import APIRouter, Depends
from app.appointments.dao import AppointmentDAO
from app.appointments.schemas import SAppointment, SAppointmentUpdate
from app.appointments.dependencies import get_current_provider
from app.appointments.models import Appointment
from app.exceptions import AccessDenied

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

@router.get("/all")
async def get_appointments(user_providers: Appointment = Depends(get_current_provider)):
    if not user_providers:
        raise AccessDenied
    provider_ids = [i["id"] for i in user_providers]
    return await AppointmentDAO.find_all(provider_ids)

@router.get("/appointment_{appointment_id}")
async def get_appointment(appointment_id: int, user_providers: Appointment = Depends(get_current_provider)):
    if not user_providers:
        raise AccessDenied
    appointment = await AppointmentDAO.find_one_or_none(id=appointment_id)    
    if appointment is None:
        raise AccessDenied
    provider_ids = [i["id"] for i in user_providers]
    if appointment["provider_id"] not in provider_ids:
        raise AccessDenied
    return appointment

@router.post("/add")
async def add_appointment(appointment: SAppointment, user_providers: Appointment = Depends(get_current_provider)):
    if not user_providers:
        raise AccessDenied
    provider_ids = [i["id"] for i in user_providers]
    if appointment.provider_id not in provider_ids:
        raise AccessDenied
    values = appointment.model_dump()
    return await AppointmentDAO.add_appointment(**values)

@router.patch("/{appointment_id}")
async def update_appointment(appointment_id: int, appointment: SAppointmentUpdate, user_providers: Appointment = Depends(get_current_provider)):
    if not user_providers:
        raise AccessDenied
    provider_ids = [i["id"] for i in user_providers]
    appointment_provider = (await AppointmentDAO.find_one_or_none(id=appointment_id))['provider_id']
    if appointment_provider not in provider_ids:
        raise AccessDenied
    values = {k: v for k, v in (appointment.model_dump()).items() if v is not None}
    await AppointmentDAO.update(**values, id=appointment_id)

@router.delete("/{appointment_id}")
async def remove_appointment(appointment_id: int, user_providers: Appointment = Depends(get_current_provider)):
    if not user_providers:
        raise AccessDenied
    provider_ids = [i["id"] for i in user_providers]
    appointment_provider = (await AppointmentDAO.find_one_or_none(id=appointment_id))['provider_id']
    if appointment_provider not in provider_ids:
        raise AccessDenied
    await AppointmentDAO.delete(id=appointment_id)
