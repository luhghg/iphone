from app.repositories.product_repository import create_product, get_all_products, get_product, get_product_by_category_id, update_product, delete_product
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product_schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException, status
from app.models.bd_models import Product
from app.core.redis import redis_client, get_cache, set_cache, delete_cache
from app.schemas.product_schemas import ProductResponse


async def create_new_product(session: AsyncSession, product_data: ProductCreate) -> Product:
    product = await create_product(session=session, product_data=product_data)
    await delete_cache("products:all")
    return product
    

async def get_products(session: AsyncSession, offset: int = 0, limit: int = 100) -> list[Product]:
    if products := await get_cache("products:all"):
        return products
    else:
        products = await get_all_products(session=session, offset=offset, limit=limit)
        await set_cache("products:all", [ProductResponse.model_validate(p).model_dump() for p in products])
        return products

    if limit > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit cannot exceed 100")
    elif limit < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit must be at least 1")
    elif offset < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offset cannot be negative")
    elif offset > 1000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offset cannot exceed 1000")
    return await get_all_products(session=session, offset=offset, limit=limit)


async def get_product_by_id(session: AsyncSession, id: int) -> Product:
    if product := await get_cache(f"product:{id}"):
        return product
    if product := await get_product(session=session, id=id):
        await set_cache(f"product:{id}", ProductResponse.model_validate(product).model_dump())
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


async def get_products_by_category_id(session: AsyncSession, category_id: int) -> list[Product]:
    if not category_id: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category ID must be provided")
    if category_id < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category ID must be a positive integer")
    return await get_product_by_category_id(session=session, category_id=category_id)


async def update_product_by_id(session: AsyncSession, id: int, new_product_data: ProductUpdate) -> Product:
    product = await get_product_by_id(session=session, id=id)
    product_udated = await update_product(session=session, product=product, new_product_data=new_product_data)
    await delete_cache("products:all")
    await delete_cache(f"product:{id}")
    return product_udated


async def delete_product_by_id(session: AsyncSession, id: int) -> None:
    product = await get_product_by_id(session=session, id=id)
    await delete_product(session=session, product=product)
    await delete_cache("products:all")
    await delete_cache(f"product:{id}")

async def search_products_by_name(session: AsyncSession, query: str) -> list[Product]:
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query must be provided")
    if len(query) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query must be at least 3 characters long")
    return await get_products_by_name(session=session, query=query)




    