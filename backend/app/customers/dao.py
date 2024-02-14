
from datetime import date

from sqlalchemy import and_, func, insert, or_, select


from app.customers.models import Customer
from app.dao.base import BaseDAO
from app.database import async_session_maker

from app.logger import logger


class CustomerDAO(BaseDAO):
    model = Customer

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
                insert(Customer)
                .values(name=name,
                        birthday=birthday,
                        registration_date=registration_date,
                        rating=rating,
                        verified=verified,
                        location=location,
                        image_id=image_id,
                        score=score)
                .returning(Customer.id,
                           Customer.name)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()
