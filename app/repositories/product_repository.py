from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bd_models import Product
from app.schemas.product_schemas import ProductCreate, ProductUpdate
from sqlalchemy import select


async def create_product(session:AsyncSession, product_data: ProductCreate) -> Product:
    product = Product(
        name = product_data.name,
        description = product_data.description,
        category_id = product_data.category_id,
        is_active = product_data.is_active
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def get_all_products(session:AsyncSession, offset: int = 0, limit: int = 100) -> list[Product]:
    query = (
        select(Product)
        .offset(offset)
        .limit(limit) 
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_product(session:AsyncSession, id: int) -> Product:
    query = (
        select(Product)
        .where(Product.id == id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_product_by_category_id(session:AsyncSession, category_id: int) -> list[Product]:
    query = (
        select(Product)
        .where(Product.category_id == category_id)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def update_product(session: AsyncSession, product: Product, new_product_data: ProductUpdate) -> Product:
    if new_product_data.name is not None:
        product.name = new_product_data.name
    if new_product_data.description is not None:
        product.description = new_product_data.description
    if new_product_data.is_active is not None:
        product.is_active = new_product_data.is_active
    if new_product_data.category_id is not None:
        product.category_id = new_product_data.category_id
    await session.commit()
    await session.refresh(product)
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
    await session.commit()


