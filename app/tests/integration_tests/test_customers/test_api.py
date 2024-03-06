from datetime import datetime
from httpx import AsyncClient
import pytest
from app.tests.conftest import fastapi_app


@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "test5@example.com",
            "password": "string",
        })
        assert ac.cookies["booking_access_token"]
        yield ac

@pytest.mark.parametrize("name,birthday,registration_date,rating, \
    verified,location,image_id,score,status_code", [
    ("Elena", "1975-06-18", "2023-06-18", "100", "True", "Minsk", "23", "100", 200),
    ("Elena", "1975-06-18", "2023-06-18", "100", "True", "Minsk", "23", "100", 409),
])
async def test_add_customer(name, birthday, registration_date, rating, verified,
                            location, image_id, score, status_code, authenticated_ac: authenticated_ac):
    response = await authenticated_ac.post("/customers/add", json={
        "name": name,
        "birthday": birthday,
        "registration_date": registration_date,
        "rating": rating,
        "verified": verified,
        "location": location,
        "image_id": image_id,
        "score": score
    })

    assert response.status_code == status_code