from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_image_services import get_product_image_by_id, delete_product_image_by_id, update_product_image_by_id, get_products_images_by_product_id_service, create_new_product_image
from app.schemas.product_image_schemas import ProductImageCreate, ProductImageResponse, ProductImageUpdate
from app.db.session import get_session
from app.services.auth_services import  get_current_admin


router = APIRouter(prefix="/product-image", tags=["ProductImage"])


@router.post("/", response_model=ProductImageResponse)
async def create_new_product_image_api(product_image : ProductImageCreate, session: AsyncSession = Depends(get_session), current_user = Depends(get_current_admin)):
    return await create_new_product_image(session=session, image_data=product_image)

@router.get("/product/{product_id}", response_model=list[ProductImageResponse])
async def get_product_image_by_product_id_api(product_id : int ,session: AsyncSession = Depends(get_session)):
    return await get_products_images_by_product_id_service(session=session, product_id=product_id)


@router.get("/{id}", response_model=ProductImageResponse)
async def get_product_image_by_id_api(id: int, session: AsyncSession = Depends(get_session)):
    return await get_product_image_by_id(session=session, id=id)


@router.put("/{id}", response_model=ProductImageResponse)
async def update_product_image_by_id_api(id: int, new_image_data: ProductImageUpdate, session: AsyncSession = Depends(get_session), current_user = Depends(get_current_admin)):
    return await update_product_image_by_id(session=session, id=id, new_product_image=new_image_data )


@router.delete("/{id}", status_code=204)
async def delete_product_image_by_id_api(id: int,  session: AsyncSession = Depends(get_session), current_user = Depends(get_current_admin)):
    return await delete_product_image_by_id(session = session, id=id)

