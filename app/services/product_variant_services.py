from app.repositories.product_variant_repository import create_product_variant, get_product_variant, get_all_product_variants, get_product_variants_by_product_id, update_product_variant, delete_product_variant
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product_variant_schemas import ProductVariantCreate, ProductVariantUpdate
from fastapi import HTTPException, status
from app.models.bd_models import ProductVariant


async def create_new_product_variant(session: AsyncSession, variant_data: ProductVariantCreate) -> ProductVariant:
    return await create_product_variant(session=session, variant_data=variant_data)


async def get_product_variant_by_id(session: AsyncSession, id: int) -> ProductVariant:
    if variant := await get_product_variant(session=session, id=id):
        return variant
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product variant not found")


async def get_products_variants(session: AsyncSession, offset: int = 0, limit: int = 100) -> list[ProductVariant]:
    if limit > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit cannot exceed 100")
    elif limit < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit must be at least 1")
    elif offset < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offset cannot be negative")
    elif offset > 1000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offset cannot exceed 1000")
    return await get_all_product_variants(session=session, offset=offset, limit=limit)


async def get_product_variants_by_product_id_service(session: AsyncSession, product_id: int) -> list[ProductVariant]:
    if not product_id: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be provided")
    if product_id < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be a positive integer")
    return await get_product_variants_by_product_id(session=session, product_id=product_id)


async def update_product_variant_by_id(session: AsyncSession, id: int, new_data: ProductVariantUpdate) -> ProductVariant:
    variant = await get_product_variant_by_id(session=session, id=id)
    return await update_product_variant(session=session, variant=variant, new_data=new_data)


async def delete_product_variant_by_id(session: AsyncSession, id: int) -> None:
    variant = await get_product_variant_by_id(session=session, id=id)
    await delete_product_variant(session=session, variant=variant)



