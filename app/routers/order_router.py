from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_services import (create_new_order, get_orders_by_user,
                                          get_order_by_id, update_order_status)
from app.schemas.order_schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from app.db.session import get_session
from app.services.auth_services import get_current_user, get_current_admin
from app.models.bd_models import User


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order_router(
    order_data: OrderCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_new_order(session=session, user_id=current_user.id, order_data=order_data)


@router.get("", response_model=list[OrderResponse])
async def get_my_orders_router(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_orders_by_user(session=session, user_id=current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_router(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_order_by_id(session=session, order_id=order_id, user_id=current_user.id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status_router(
    order_id: int,
    status_update: OrderStatusUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin),
):
    return await update_order_status(session=session, order_id=order_id, status_update=status_update)
