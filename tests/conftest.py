from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env.test", override=True)

import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from app.db.session import async_engine, Base


def pytest_sessionstart(session):
    async def _create():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await async_engine.dispose()
    asyncio.run(_create())


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
