from sqlalchemy import insert
from app.appointments.models import Appointment
from app.dao.base import BaseDAO
from app.database import async_session_maker


class AppointmentDAO(BaseDAO):
    model = Appointment

    @classmethod
    async def add_appointment(
        cls,
        provider_id: int,
        customer_id: int,
        offer: str,
        datetime_from,
        datetime_to,
        price: int
    ):
        '''

        '''
        async with async_session_maker() as session:
            stmt = (
                insert(Appointment)
                .values(provider_id=provider_id,
                        customer_id=customer_id,
                        offer=offer,
                        datetime_from=datetime_from,
                        datetime_to=datetime_to,
                        price=price)
                .returning(Appointment.id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()
