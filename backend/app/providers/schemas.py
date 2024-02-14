from datetime import date
from typing import Any, Optional, Union

from pydantic import BaseModel


class SProvider(BaseModel):
    id: int
    name: str
    foundation_date: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    tags: list | Any

    class Config:
        from_attributes = True

class SNewProvider(BaseModel):
    name: str
    foundation_date: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    tags: list

    class Config:
        from_attributes = True
