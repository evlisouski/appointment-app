
from datetime import date

from sqlalchemy import and_, func, insert, or_, select


from app.customers.models import Customers
from app.dao.base import BaseDAO
from app.database import async_session_maker

from app.logger import logger


class CustomerDAO(BaseDAO):
    model = Customers

    @classmethod
    async def get_customers(cls, customer_id: int):
        """SELECT * FROM customers"""
        async with async_session_maker() as session:

            query = (
                select(Customers.name)
                .select_from(Customers)
                .where(Customers.id == customer_id)
            )

            result = await session.execute(query)
            return result

    @classmethod
    async def add_customer(
        cls,
        name: str,
        birthday: date,
        registration_date: date,
        rating: int,
        verified: bool,
        location: str,
        image_id: int,
        score: int
    ):
        '''
        INSERT INTO customers
        ("name", "birthday", "registration_date", "rating", "verified",
        "location", "image_id", "score")
        VALUES
        ('Eduard', '1992-07-20', '2024-01-01', 100, TRUE,
        'Minsk', 1, 123);
        '''
        async with async_session_maker() as session:
            stmt = (
                insert(Customers)
                .values(name=name,
                        birthday=birthday,
                        registration_date=registration_date,
                        rating=rating,
                        verified=verified,
                        location=location,
                        image_id=image_id,
                        score=score)
                .returning(Customers.id,
                           Customers.name)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.all()
