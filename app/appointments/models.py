import datetime
import pytz
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    provider_id = mapped_column(Integer, ForeignKey("providers.id", ondelete="CASCADE"))
    customer_id = Column(BigInteger, default=None)
    offer = Column(String, nullable=False)
    datetime_from = Column(DateTime(timezone=True),
                           default=datetime.datetime.now(tz=pytz.timezone('UTC')),
                           nullable=False)
    datetime_to = Column(DateTime(timezone=True),
                         default=datetime.datetime.now(tz=pytz.timezone('UTC')),
                         nullable=False)
    price = Column(Integer, nullable=False)

    providers = relationship("Provider", back_populates="appointments")

    def __str__(self):
        return f"Appointment #{self.id}"
