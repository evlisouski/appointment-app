import asyncio
from typing import Optional
from fastapi import APIRouter, Depends
from app.appointments.dao import AppointmentDAO
from app.appointments.schemas import SAppointment, SAppointmentUpdate
from app.appointments.dependencies import get_current_provider
from app.appointments.models import Appointment
from app.exceptions import AccessDenied, UserIsNotPresentException
from app.users.dependencies import get_current_user 
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.get("/all")
@cache(expire=3)
async def get_appointments(user_providers: Appointment = Depends(get_current_provider)):    
    if not user_providers:
        raise AccessDenied
    provider_ids = [i["id"] for i in user_providers]
    return await AppointmentDAO.find_all(provider_ids)

@router.get("/available_appointments")
async def get_available_appointments(user_providers: Appointment = Depends(get_current_provider)):
    if not user_providers:
        raise AccessDenied    
    return await AppointmentDAO.find_all_free()

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
    
@router.patch("/book_appointtment/{appointment_id}")
async def book_appointtment(appointment_id: int, current_user: Appointment = Depends(get_current_user)):
    if not current_user:
        raise UserIsNotPresentException
    appointment = await AppointmentDAO.find_one_or_none(id=appointment_id)    
    if not appointment or appointment["customer_id"] != None:
        raise AccessDenied        
    await AppointmentDAO.update(id=appointment_id, customer_id=current_user["id"])
    return "Done"

@router.patch("/cancel_appointtment/{appointment_id}")
async def book_appointtment(appointment_id: int, current_user: Appointment = Depends(get_current_user)):
    if not current_user:
        raise UserIsNotPresentException
    appointment = await AppointmentDAO.find_one_or_none(id=appointment_id)    
    if not appointment or appointment["customer_id"] != current_user["id"]:
        raise AccessDenied        
    await AppointmentDAO.update(id=appointment_id, customer_id=None)
    return "Done"
    
