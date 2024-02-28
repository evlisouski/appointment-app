import httpx
import pytest

@pytest.mark.
def test_customers():
    response = httpx.post('http://127.0.0.1:8000/auth/login',
                          json={"email": "test5@example.com",
                                "password": "string"})
    print(response.request._content)
    
