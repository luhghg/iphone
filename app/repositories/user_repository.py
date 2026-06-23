from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.bd_models import User
from sqlalchemy import select
from fastapi import HTTPException, status

from app.schemas.user_schemas import UserCreate

async def get_user_by_email(session: AsyncSession, email: str) -> User:
    query = (select(User)
             .where(User.email == email))

    result = await session.execute(query)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    session.add(user_data)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    await session.refresh(user_data)
    return user_data

async def get_by_id(session: AsyncSession, id: int) -> User:
    query = (
        select(User)
        .where(User.id == id))
    result = await session.execute(query)
    return result.scalar_one_or_none()