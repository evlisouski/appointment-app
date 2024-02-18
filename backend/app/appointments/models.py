from sqlalchemy import JSON, BigInteger, Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, String, SmallInteger, true
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    provider_id = mapped_column(Integer, ForeignKey("providers.id", ondelete="CASCADE"), primary_key=True, )
    customer_id = Column(BigInteger, default=None)
    user_id = None
    offer = Column(String, nullable=False)
    datetime_from = Column(DateTime, nullable=False)
    datetime_to = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)
    
    provider = relationship("Provider", back_populates="appointments")

    def __str__(self):
        return f"Booking #{self.id}"
