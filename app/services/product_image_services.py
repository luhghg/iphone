from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.product_image_repository import create_product_image, get_product_images_by_product_id, get_product_image_one, update_product_image, delete_product_image
from app.schemas.product_image_schemas import ProductImageCreate, ProductImageUpdate
from app.models.bd_models import ProductImage


async def create_new_product_image(session: AsyncSession, image_data: ProductImageCreate) -> ProductImage:
    return await create_product_image(session=session, image_data=image_data)


async def get_products_images_by_product_id_service(session: AsyncSession, product_id: int) -> list[ProductImage]:
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product_id < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID can not be negtive or 0")
    return await get_product_images_by_product_id(session=session, product_id=product_id)


async def get_product_image_by_id(session: AsyncSession, id: int) -> ProductImage:
    if product_image := await get_product_image_one(session=session, id=id):
        return product_image
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


async def update_product_image_by_id(session: AsyncSession, id: int, new_product_image: ProductImageUpdate):
    product_image = await get_product_image_by_id(session=session, id=id)
    return await update_product_image(session=session, product_image=product_image, new_image_data=new_product_image)


async def delete_product_image_by_id(session: AsyncSession, id: int ) -> None:
    product_image = await get_product_image_by_id(session=session, id=id)
    await delete_product_image(session=session, product_image=product_image)







    
    