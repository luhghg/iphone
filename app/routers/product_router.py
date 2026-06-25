from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_services import (create_new_product, get_products, get_product_by_id,
                                           get_products_by_category_id,update_product_by_id,
                                           delete_product_by_id, search_products_by_name)
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductResponse
from app.db.session import get_session
from app.services.auth_services import  get_current_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, session: AsyncSession = Depends(get_session), current_user = Depends(get_current_admin)):
    return await create_new_product(session=session, product_data=product_data)


@router.get("/", response_model=list[ProductResponse])
async def read_products(session: AsyncSession = Depends(get_session)):
    return await get_products(session=session)

@router.get('/search', response_model=list[ProductResponse])
async def search_products(query: str, session: AsyncSession = Depends(get_session)):
    return await search_products_by_name(session=session, query=query)


@router.get("/category/{category_id}", response_model=list[ProductResponse])
async def read_products_by_category(category_id: int, session: AsyncSession = Depends(get_session)):
    return await get_products_by_category_id(session=session, category_id=category_id)  


@router.get("/{id}", response_model=ProductResponse)
async def read_product(id: int, session: AsyncSession = Depends(get_session)):
    return await get_product_by_id(session=session, id=id)


@router.put("/{id}", response_model=ProductResponse)
async def update_product(id: int, product_data: ProductUpdate, session: AsyncSession = Depends(get_session), current_user = Depends(get_current_admin)):
    return await update_product_by_id(session=session, id=id, new_product_data=product_data)


@router.delete("/{id}", status_code=204)
async def delete_product(id: int, session: AsyncSession = Depends(get_session), current_user = Depends(get_current_admin)):
    await delete_product_by_id(session=session, id=id)


