import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert
from app.config import settings
from app.database import Base, async_session_maker, engine

from app.customers.models import Customer
from app.providers.models import Provider, ProviderTag, Tag

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
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    customers = open_mock_json("customers")
    providers = open_mock_json("providers")
    tags = open_mock_json("tags")
    providers_tags = open_mock_json("providers_tags")

    for customer in customers:
        customer["birthday"] = datetime.strptime(customer["birthday"], "%Y-%m-%d")
        customer["registration_date"] = datetime.strptime(customer["registration_date"], "%Y-%m-%d")

    for provider in providers:
        provider["foundation_date"] = datetime.strptime(provider["foundation_date"], "%Y-%m-%d")
        provider["registration_date"] = datetime.strptime(provider["registration_date"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_customers = insert(Customer).values(customers)
        add_providers = insert(Provider).values(providers)
        add_tags = insert(Tag).values(tags)
        add_providers_tags = insert(ProviderTag).values(providers_tags)

        await session.execute(add_customers)
        await session.execute(add_providers)
        await session.execute(add_tags)
        await session.execute(add_providers_tags)

        await session.commit()

# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
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


