from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SAppointment(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    provider_id: int
    customer_id: int | None
    offer: str
    datetime_from: datetime
    datetime_to: datetime
    price: int


class SAppointmentUpdate(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    customer_id: Optional[int] = None
    offer: Optional[str] = None
    datetime_from: Optional[datetime] = None
    datetime_to: Optional[datetime] = None
    price: Optional[int] = None
