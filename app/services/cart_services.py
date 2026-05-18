from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.cart_repository import (create_cart_repo,
                                              get_cart_by_user_id_repo,
                                              add_item_to_cart_repo,
                                              get_cart_item_by_id_repo,
                                              get_cart_item_by_variant_repo,
                                              get_cart_items_by_cart_id_repo,
                                              update_cart_item_quantity_repo,
                                              increment_cart_item_quantity_repo,
                                              delete_cart_item_repo,
                                              delete_all_cart_items_repo)
from app.repositories.product_variant_repository import get_product_variant
from app.schemas.cart_schemas import CartItemCreate, CartResponse, CartItemUpdate
from app.models.bd_models import Cart, CartItem


async def get_or_create_cart_service(session: AsyncSession, user_id: int ) -> Cart:
    cart = await get_cart_by_user_id_repo(session=session, user_id=user_id)
    if cart is None:
        cart = await create_cart_repo(session=session, user_id= user_id)
    return cart
    
        
async def add_item_to_cart_service(session: AsyncSession, user_id: int, cart_item_data: CartItemCreate) -> CartItem:
    variant = await get_product_variant(session=session, id=cart_item_data.product_variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")

    cart = await get_or_create_cart_service(session=session, user_id=user_id)

    existing_item = await get_cart_item_by_variant_repo(
        session=session, cart_id=cart.id, product_variant_id=cart_item_data.product_variant_id
    )
    if existing_item:
        return await increment_cart_item_quantity_repo(
            session=session, cart_item=existing_item, amount=cart_item_data.quantity
        )

    return await add_item_to_cart_repo(session=session, cart_id=cart.id, cart_item_data=cart_item_data)


async def get_cart_item_by_id_service(session: AsyncSession, user_id: int, id: int) -> CartItem:
    cart = await get_cart_by_user_id_repo(session=session, user_id=user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = await get_cart_item_by_id_repo(session=session, id=id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if cart_item.cart_id != cart.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return cart_item


async def get_cart_service(session: AsyncSession, user_id: int) -> CartResponse :
    cart = await get_cart_by_user_id_repo(session=session, user_id=user_id)
    if not cart:
        cart = await get_or_create_cart_service(session=session, user_id=user_id)
    return cart 


async def update_cart_item_service(session: AsyncSession, user_id: int, id: int, item_data: CartItemUpdate) -> CartItem:
    cart = await get_cart_by_user_id_repo(session=session, user_id=user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = await get_cart_item_by_id_repo(session=session, id=id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if cart_item.cart_id != cart.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if item_data.quantity is not None and item_data.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    return await update_cart_item_quantity_repo(session=session, cart_item=cart_item, quantity=item_data)


async def delete_cart_item_service(session: AsyncSession, user_id: int, id: int) -> None:
    cart = await get_cart_by_user_id_repo(session=session, user_id=user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = await get_cart_item_by_id_repo(session=session, id=id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if cart_item.cart_id != cart.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return await delete_cart_item_repo(session=session, cart_item=cart_item)


async def delete_all_cart_items_service(session: AsyncSession, user_id: int ) -> None:
    cart = await get_cart_by_user_id_repo(session=session, user_id=user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    carts_items = await get_cart_items_by_cart_id_repo(session=session, cart_id=cart.id)
    return await delete_all_cart_items_repo(session=session, carts_items=carts_items)



    








