
async def test_register(client):
    response = await client.post(
        "/auth/register", json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200


async def test_same_email(client):
    response = await client.post("/auth/register", json={"username": "testuser2", "email":"test@example.com", "password": "testpassword2"})
    response2 = await client.post("/auth/register", json={"username": "testuser3", "email":"test@example.com", "password": "testpassword3"})
    assert response.status_code == 200
    assert response2.status_code == 400
    

async def test_login_success(client):
    response = await client.post("/auth/register", json={"username": "testuser", "email":"test@gmail.com", "password": "testpassword"})
    assert response.status_code == 200
    response = await client.post("/auth/login", json={"email": "test@gmail.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password(client):
    response = await client.post("/auth/register", json={"username": "testuser", "email":"test@gmail.com", "password": "testpassword"})
    assert response.status_code == 200
    response = await client.post("/auth/login", json={"email": "test@gmail.com", "password": "wrongpassword"})
    assert response.status_code == 401

