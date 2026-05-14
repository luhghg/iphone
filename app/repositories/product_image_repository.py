from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bd_models import ProductImage
from app.schemas.product_image_schemas import ProductImageCreate, ProductImageUpdate
from sqlalchemy import select


async def create_product_image(session: AsyncSession, image_data: ProductImageCreate) -> ProductImage:
    product_image = ProductImage(
        product_id = image_data.product_id,
        image_url = image_data.image_url,
        is_main = image_data.is_main
    )
    session.add(product_image)
    await session.commit()
    await session.refresh(product_image)
    return product_image


async def get_product_images_by_product_id(session: AsyncSession, product_id: int) -> list[ProductImage]:
    query = (
        select(ProductImage)
        .where(ProductImage.product_id == product_id)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_product_image_one(session: AsyncSession, id: int) -> ProductImage:
    query = (
        select(ProductImage)
        .where(ProductImage.id == id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_product_image(session: AsyncSession, product_image: ProductImage, new_image_data: ProductImageUpdate) -> ProductImage:
    if new_image_data.image_url is not None:
        product_image.image_url = new_image_data.image_url
    if new_image_data.is_main is not None:
        product_image.is_main = new_image_data.is_main
    await session.commit()
    await session.refresh(product_image)
    return product_image


async def delete_product_image(session: AsyncSession, product_image: ProductImage) -> None:
    await session.delete(product_image)
    await session.commit()