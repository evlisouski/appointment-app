from sqlalchemy import insert
from app.customers.models import Customer
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.logger import logger

class CustomerDAO(BaseDAO):
    model = Customer

    @classmethod
    async def add_customer(cls, **values):
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
                .values(values)
                .returning(Customer.id,
                           Customer.name)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()
