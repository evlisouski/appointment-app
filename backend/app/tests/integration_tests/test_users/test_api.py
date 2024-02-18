import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("ex@ample.com", "example", 201),
    ("ex@ample.com", "example", 409),
    ("test10@example.com", "test10example", 201),
    ("abcde", "example", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("ex@ample.com", "example", 200),
    ("test10@example.com", "test10example", 200),
    ("wrong@person.com", "testtest", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
