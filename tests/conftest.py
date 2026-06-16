import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env.test", override=True)

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.session import Base, get_session
from main import app


test_engine = create_async_engine(settings.DATABASE_URL_asyncpg, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(autouse=True)
async def clean_db():
    yield
    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture
async def auth_headers(client):
    await client.post("/auth/register", json={"username": "testuser", "email": "test@gmail.com", "password": "testpassword"})
    login = await client.post("/auth/login", json={"email": "test@gmail.com", "password": "testpassword"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.fixture
async def admin_headers(client):
    from sqlalchemy import update
    from app.models.bd_models import User

    await client.post("/auth/register", json={"username": "admin", "email": "admin@test.com", "password": "adminpassword"})
    async with TestSessionLocal() as session:
        await session.execute(update(User).where(User.email == "admin@test.com").values(role="admin"))
        await session.commit()
    login = await client.post("/auth/login", json={"email": "admin@test.com", "password": "adminpassword"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.fixture
async def product_variant(client, admin_headers):
    cat = await client.post("/categories/", json={"name": "Phones", "slug": "phones"}, headers=admin_headers)
    prod = await client.post("/products/", json={"name": "iPhone", "description": "test", "category_id": cat.json()["id"]}, headers=admin_headers)
    variant = await client.post("/product-variants/", json={"product_id": prod.json()["id"], "price": 999.0, "stock": 10}, headers=admin_headers)
    return variant.json()
