from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bd_models import Order, OrderItem
from app.schemas.order_schemas import OrderCreate, OrderStatusUpdate, OrderItemCreate
from sqlalchemy import select


async def create_order_repo(session: AsyncSession, user_id: int, total_price: float, order_data: OrderCreate) -> Order:
    order = Order(
        user_id=user_id,
        status="pending",
        total_price=total_price,
        delivery_address=order_data.delivery_address
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def create_order_item_repo(session: AsyncSession, item_data: OrderItemCreate) -> OrderItem:
    item = OrderItem(order_id=item_data.order_id,
                     product_variant_id=item_data.product_variant_id,
                     quantity=item_data.quantity,
                     price_at_purchase=item_data.price_at_purchase                    
    )
    session.add(item) 
    await session.commit()
    await session.refresh(item)
    return item


async def get_orders_by_user_repo(session: AsyncSession, user_id: int) -> list[Order]:
    result = await session.execute(select(Order).where(Order.user_id == user_id))
    return result.scalars().all()


async def get_order_by_id_repo(session: AsyncSession, order_id: int) -> Order:
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def update_order_status_repo(session: AsyncSession, order_id: int, status_update: OrderStatusUpdate) -> Order:
    order = await get_order_by_id_repo(session, order_id)
    if order:
        order.status = status_update.status
        await session.commit()
        await session.refresh(order)
    return order






