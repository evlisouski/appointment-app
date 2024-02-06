from sqlalchemy import JSON, Boolean, Column, Date, Integer, String, SmallInteger
from sqlalchemy.orm import relationship

from app.database import Base


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=256), nullable=False)
    birthday = Column(Date, nullable=True)
    registration_date = Column(Date, nullable=False)
    rating = Column(SmallInteger, nullable=True, default=0)
    verified = Column(Boolean, nullable=False, default=False)
    location = Column(String, nullable=False)
    image_id = Column(Integer)
    score = Column(SmallInteger)

    def __str__(self):
        return f"Customer {self.name}"
