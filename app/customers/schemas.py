from datetime import date
from typing import Optional
from unittest.mock import Base
from fastapi import Depends

from pydantic import BaseModel, ConfigDict

from app.users.models import User
from app.users.dependencies import get_current_user


class SCustomer(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: int
    name: str
    birthday: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    score: int


class SNewCustomer(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    name: str
    birthday: date
    registration_date: date
    rating: int
    verified: bool
    location: str
    image_id: int
    score: int


class SNewCustomerReturn(BaseModel):
    id: int
    name: str
