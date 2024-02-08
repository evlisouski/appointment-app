from datetime import date
from typing import Optional
from unittest.mock import Base

from pydantic import BaseModel


class SCustomer(BaseModel):
    id: int
    name: str
    birthday: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    score: int

    class Config:
        from_attributes = True


class SNewCustomer(BaseModel):
    name: str
    birthday: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    score: int

    class Config:
        from_attributes = True


class SNewCustomerReturn(BaseModel):
    id: int
    name: str
