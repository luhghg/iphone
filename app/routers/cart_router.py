from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.cart_services import (
    add_item_to_cart_service,
    get_cart_item_by_id_service,
    get_cart_service,
    update_cart_item_service,
    delete_cart_item_service,
    delete_all_cart_items_service,
)
from app.schemas.cart_schemas import CartItemResponse, CartItemCreate, CartResponse, CartItemUpdate
from app.db.session import get_session
from app.services.auth_services import get_current_user
from app.models.bd_models import User


router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
async def get_cart_router(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_cart_service(session=session, user_id=current_user.id)


@router.post("/items", response_model=CartItemResponse, status_code=201)
async def add_item_to_cart_router(
    cart_item_data: CartItemCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await add_item_to_cart_service(session=session, user_id=current_user.id, cart_item_data=cart_item_data)


@router.get("/items/{id}", response_model=CartItemResponse)
async def get_cart_item_by_id_router(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_cart_item_by_id_service(session=session, id=id, user_id=current_user.id)


@router.patch("/items/{id}", response_model=CartItemResponse)
async def update_cart_item_router(
    id: int,
    item_data: CartItemUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_cart_item_service(session=session, id=id, user_id=current_user.id, item_data=item_data)


@router.delete("/items/{id}", status_code=204)
async def delete_cart_item_router(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await delete_cart_item_service(session=session, id=id, user_id=current_user.id)


@router.delete("/items", status_code=204)
async def delete_all_cart_items_router(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await delete_all_cart_items_service(session=session, user_id=current_user.id)
