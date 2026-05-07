from app.schemas.user_schemas import UserCreate, UserLogin, Token, UserResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import ExpiredSignatureError, JWTError, jwt
from app.core.config import settings as settings
from app.db.session import get_session
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import create_user, get_by_id, get_user_by_email
from app.models.bd_models import User

oauth2_scheme = HTTPBearer()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": exp})
    encoded_jwt  = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(session: AsyncSession = Depends(get_session), credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    func_get_id = await get_by_id(session, int(user_id))
    if func_get_id is None:
        raise HTTPException(status_code=404, detail="Invalid token")
    return func_get_id


async def register_user(session: AsyncSession, user_data: UserCreate) -> UserResponse:
    if await get_user_by_email(session=session, email=user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hash_pass = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_pass
    )
    create_new_user = await create_user(session=session, user_data=new_user)
    return create_new_user

async def login_user(session: AsyncSession, login_data: UserLogin) -> Token:
    user = await get_user_by_email(session=session, email=login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)





 
# 
 