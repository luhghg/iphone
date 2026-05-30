from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.order_repository import (create_order_repo, create_order_item_repo,
                                                get_orders_by_user_repo, get_order_by_id_repo,
                                                update_order_status_repo)
from app.repositories.cart_repository import (get_cart_by_user_id_repo,
                                               get_cart_items_by_cart_id_repo,
                                               delete_all_cart_items_repo)
from app.repositories.product_variant_repository import get_product_variant
from app.schemas.order_schemas import OrderCreate, OrderStatusUpdate, OrderItemCreate
from app.models.bd_models import Order


async def create_new_order(session: AsyncSession, user_id: int, order_data: OrderCreate) -> Order:
    # 1. Отримуємо корзину
    cart = await get_cart_by_user_id_repo(session=session, user_id=user_id)
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    cart_items = await get_cart_items_by_cart_id_repo(session=session, cart_id=cart.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 2. Перевіряємо stock і рахуємо total_price
    total_price = 0.0
    items_with_variants = []
    for item in cart_items:
        variant = await get_product_variant(session=session, id=item.product_variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail=f"Product variant {item.product_variant_id} not found")
        if variant.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for variant {item.product_variant_id}")
        total_price += variant.price * item.quantity
        items_with_variants.append((item, variant))

    # 3. Створюємо Order
    order = await create_order_repo(session=session, user_id=user_id,
                                    total_price=total_price, order_data=order_data)

    # 4. Створюємо OrderItem для кожного товару + зменшуємо stock
    for item, variant in items_with_variants:
        order_item_data = OrderItemCreate(
            order_id=order.id,
            product_variant_id=item.product_variant_id,
            quantity=item.quantity,
            price_at_purchase=variant.price
        )
        await create_order_item_repo(session=session, item_data=order_item_data)
        variant.stock -= item.quantity
        await session.commit()

    # 5. Очищаємо корзину
    await delete_all_cart_items_repo(session=session, carts_items=cart_items)

    await session.refresh(order)
    return order


async def get_orders_by_user(session: AsyncSession, user_id: int) -> list[Order]:
    return await get_orders_by_user_repo(session=session, user_id=user_id)


async def get_order_by_id(session: AsyncSession, order_id: int, user_id: int) -> Order:
    order = await get_order_by_id_repo(session=session, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return order


async def update_order_status(session: AsyncSession, order_id: int, status_update: OrderStatusUpdate) -> Order:
    order = await update_order_status_repo(session=session, order_id=order_id, status_update=status_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
