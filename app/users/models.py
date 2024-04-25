from sqlalchemy import Column, Integer, Nullable, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")

    customers = relationship("Customer", back_populates="users")
    providers = relationship("Provider", back_populates="users")

    def __str__(self):
        return f"{self.email}"