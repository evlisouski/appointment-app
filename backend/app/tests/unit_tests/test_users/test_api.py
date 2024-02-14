from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("name,birthday,registration_date,rating, \
    verified,location,image_id,score,status_code", [
("Elena", "1975-06-18", "2023-06-18", "100", "True", "Minsk", "23", "100", 200),
("Elena", "1975-06-18", "2023-06-18", "100", "True", "Minsk", "23", "100", 200),
])
async def test_add_customer(name, birthday, registration_date, rating, verified, location, image_id, score, status_code, ac: AsyncClient):
    response = await ac.post("/customers/add", json={
        "name": name,
        "birthday": birthday,
        "registration_date": registration_date,
        "rating": rating,
        "verified": verified,
        "location": location,
        "image_id": image_id,
        "score": score
    })

    print("--------------------------------------")
    print(response)
    assert response.status_code == status_code
