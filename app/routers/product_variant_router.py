from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_variant_services import (create_new_product_variant, get_products_variants, get_product_variant_by_id,
                                                  get_product_variants_by_product_id_service, update_product_variant_by_id,
                                                  delete_product_variant_by_id)
from app.schemas.product_variant_schemas import ProductVariantCreate, ProductVariantUpdate, ProductVariantResponse
from app.db.session import get_session
from app.services.auth_services import  get_current_admin


router = APIRouter(prefix="/product-variants", tags=["Product Variants"])


@router.post("/", response_model=ProductVariantResponse)
async def create_product_variant(variant_data: ProductVariantCreate, session: AsyncSession = Depends(get_session),
                                 current_user = Depends(get_current_admin)):
    return await create_new_product_variant(session=session, variant_data=variant_data)


@router.get("/products/{product_id}", response_model=list[ProductVariantResponse])
async def read_product_variants_by_product_id(product_id: int, session: AsyncSession = Depends(get_session)):
    return await get_product_variants_by_product_id_service(session=session, product_id=product_id)



@router.get("/variants/{id}", response_model=ProductVariantResponse)
async def read_product_variant_by_id(id: int, session: AsyncSession = Depends(get_session)):
    return await get_product_variant_by_id(session=session, id=id)


@router.get("/", response_model=list[ProductVariantResponse])
async def read_product_variants(session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = 100):
    return await get_products_variants(session=session, offset=offset, limit=limit)


@router.put("/{id}", response_model=ProductVariantResponse)
async def update_product_variant(id: int, variant_data: ProductVariantUpdate, session: AsyncSession = Depends(get_session),
                                 current_user = Depends(get_current_admin)):
    return await update_product_variant_by_id(session=session, id=id, new_data=variant_data)


@router.delete("/{id}", status_code=204)
async def delete_product_variant(id: int, session: AsyncSession = Depends(get_session), current_user = Depends(get_current_admin)):
    await delete_product_variant_by_id(session=session, id=id)



