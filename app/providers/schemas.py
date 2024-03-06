from datetime import date
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict


class SProvider(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: int
    name: str
    foundation_date: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    tags: list | Any


class SNewProvider(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    name: str
    foundation_date: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    tags: list
