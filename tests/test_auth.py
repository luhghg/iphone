import pytest 
from tests.conftest import client


async def test_register(client):
    response = await client.post(
        "/auth/register", json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
