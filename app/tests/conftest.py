import sys
from os.path import abspath, dirname

import dateutil
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from dateutil import parser
import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert
from app.config import settings
from app.database import Base, async_session_maker, engine

from app.customers.models import Customer
from app.users.models import User
from app.providers.models import Provider, ProviderTag, Tag
from app.appointments.models import Appointment

from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    customers = open_mock_json("customers")
    providers = open_mock_json("providers")
    tags = open_mock_json("tags")
    providers_tags = open_mock_json("providers_tags")
    appointments = open_mock_json("appointments")

    for customer in customers:
        customer["birthday"] = datetime.strptime(customer["birthday"], "%Y-%m-%d")
        customer["registration_date"] = datetime.strptime(customer["registration_date"], "%Y-%m-%d")

    for provider in providers:
        provider["foundation_date"] = datetime.strptime(provider["foundation_date"], "%Y-%m-%d")
        provider["registration_date"] = datetime.strptime(provider["registration_date"], "%Y-%m-%d")

    for appointment in appointments:
        appointment["datetime_from"] = parser.parse(appointment["datetime_from"])
        appointment["datetime_to"] = parser.parse(appointment["datetime_to"])

    async with async_session_maker() as session:
        add_users = insert(User).values(users)
        add_customers = insert(Customer).values(customers)
        add_providers = insert(Provider).values(providers)
        add_tags = insert(Tag).values(tags)
        add_providers_tags = insert(ProviderTag).values(providers_tags)
        add_appointments = insert(Appointment).values(appointments)

        await session.execute(add_users)
        await session.execute(add_customers)
        await session.execute(add_providers)
        await session.execute(add_tags)
        await session.execute(add_providers_tags)
        await session.execute(add_appointments)

        await session.commit()

# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
# @pytest.fixture(scope="session")
@pytest.mark.asyncio(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "test1@example.com",
            "password": "string",
        })
        assert ac.cookies["booking_access_token"]
        yield ac
