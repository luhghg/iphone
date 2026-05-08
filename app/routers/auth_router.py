from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.user_schemas import Token, UserCreate, UserLogin, UserResponse
from app.services.auth_services import login_user, register_user
from app.services.auth_services import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserResponse:
    return await register_user(session=session, user_data=user_data)


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)) -> Token:
    return await login_user(session=session, login_data=login_data)


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user 

