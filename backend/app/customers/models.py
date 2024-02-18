from sqlalchemy import JSON, Boolean, Column, Date, ForeignKey, Integer, String, SmallInteger, true
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    # id = Column(Integer, primary_key=True, autoincrement=True)
    id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, )
    name = Column(String(length=256), nullable=False)
    birthday = Column(Date, nullable=True)
    registration_date = Column(Date, nullable=False)
    rating = Column(SmallInteger, nullable=True, default=0)
    verified = Column(Boolean, nullable=False, default=False)
    location = Column(String, nullable=False)
    image_id = Column(Integer)
    score = Column(SmallInteger)
    users = relationship("User", back_populates="customers")

    def __str__(self):
        return f"Customer {self.name}"
