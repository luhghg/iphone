from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bd_models import ProductVariant
from app.schemas.product_variant_schemas import ProductVariantCreate, ProductVariantUpdate, ProductVariantResponse
from sqlalchemy import select


async def create_product_variant(session:AsyncSession, variant_data: ProductVariantCreate) -> ProductVariant:
    variant = ProductVariant(
        product_id = variant_data.product_id,
        price = variant_data.price,
        stock = variant_data.stock,
        storage = variant_data.storage,
        color = variant_data.color
    )
    session.add(variant)
    await session.commit()
    await session.refresh(variant)
    return variant


async def get_product_variant(session:AsyncSession, id: int) -> ProductVariant:
    query = (
        select(ProductVariant)
        .where(ProductVariant.id == id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_all_product_variants(session:AsyncSession, offset: int = 0, limit: int = 100) -> list[ProductVariant]:
    query = (
        select(ProductVariant)
        .offset(offset)
        .limit(limit) 
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_product_variants_by_product_id(session:AsyncSession, product_id: int) -> list[ProductVariant]:
    query = (
        select(ProductVariant)
        .where(ProductVariant.product_id == product_id)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def update_product_variant(session: AsyncSession, variant: ProductVariant, new_data: ProductVariantUpdate) -> ProductVariant:
    if new_data.price is not None:
        variant.price = new_data.price
    if new_data.stock is not None:
        variant.stock = new_data.stock
    if new_data.storage is not None:
        variant.storage = new_data.storage
    if new_data.color is not None:
        variant.color = new_data.color
    await session.commit()
    await session.refresh(variant)
    return variant


async def delete_product_variant(session: AsyncSession, variant: ProductVariant) -> None:
    await session.delete(variant)
    await session.commit()
