from sqlalchemy import insert, select
from app.appointments.models import Appointment
from app.dao.base import BaseDAO
from app.database import async_session_maker


class AppointmentDAO(BaseDAO):
    model = Appointment

    @classmethod
    async def add_appointment(cls, **values):
        '''

        '''
        async with async_session_maker() as session:
            stmt = (
                insert(Appointment)
                .values(values)
                .returning(Appointment.id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, user_providers: list):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.provider_id.in_(user_providers))
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def find_all_free(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.customer_id == None)
            result = await session.execute(query)
            return result.mappings().all()