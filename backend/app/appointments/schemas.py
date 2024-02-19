from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SAppointment(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    provider_id: int
    customer_id: int | None
    offer: str
    datetime_from: datetime
    datetime_to: datetime
    price: int
