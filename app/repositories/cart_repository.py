from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bd_models import Cart, CartItem
from app.schemas.cart_schemas import  CartItemCreate, CartItemUpdate
from sqlalchemy import select


async def create_cart_repo(session: AsyncSession, user_id: int) -> Cart:
    cart= Cart(user_id=user_id)
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    return cart


async def get_cart_by_user_id_repo(session: AsyncSession, user_id: int) -> Cart:
    query = (
        select(Cart)
        .where(Cart.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def add_item_to_cart_repo(session:AsyncSession, cart_id: int, cart_item_data: CartItemCreate) -> CartItem:
    cart_item = CartItem(cart_id=cart_id, product_variant_id = cart_item_data.product_variant_id, quantity = cart_item_data.quantity)
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)
    return cart_item


async def get_cart_items_by_cart_id_repo(session: AsyncSession, cart_id: int) -> list[CartItem]:
    query = (
        select(CartItem)
        .where(CartItem.cart_id == cart_id)
    ) 
    result = await session.execute(query)
    return result.scalars().all()


async def get_cart_item_by_id_repo(session: AsyncSession, id: int) -> CartItem:
    query = (
        select(CartItem)
        .where(CartItem.id == id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_cart_item_by_variant_repo(session: AsyncSession, cart_id: int, product_variant_id: int) -> CartItem | None:
    query = (
        select(CartItem)
        .where(CartItem.cart_id == cart_id, CartItem.product_variant_id == product_variant_id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def increment_cart_item_quantity_repo(session: AsyncSession, cart_item: CartItem, amount: int) -> CartItem:
    cart_item.quantity += amount
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)
    return cart_item


async def update_cart_item_quantity_repo(session: AsyncSession, cart_item : CartItem, quantity: CartItemUpdate) -> CartItem:
    if quantity is not None:
        cart_item.quantity = quantity.quantity

    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)
    return cart_item


async def delete_cart_item_repo(session: AsyncSession, cart_item: CartItem) -> None:
    await session.delete(cart_item)
    await session.commit()


async def delete_all_cart_items_repo(session: AsyncSession, carts_items: list[CartItem]) -> None:
    for cart_item in carts_items:
        await session.delete(cart_item)
    await session.commit()



    

