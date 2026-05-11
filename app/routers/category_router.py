from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.category_services import create_new_category, get_categories, get_category, update_category_by_id, delete_category_by_id
from app.schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.db.session import get_session


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
async def create_category(category_data: CategoryCreate, session: AsyncSession = Depends(get_session)):
    return await create_new_category(session=session, category_data=category_data)


@router.get("/", response_model=list[CategoryResponse])
async def read_categories(session: AsyncSession = Depends(get_session)):
    return await get_categories(session=session)


@router.get("/{id}", response_model=CategoryResponse)
async def read_category(id: int, session: AsyncSession = Depends(get_session)):
    return await get_category(session=session, id=id)


@router.put("/{id}", response_model=CategoryResponse)
async def update_category(id: int, category_data: CategoryUpdate, session: AsyncSession = Depends(get_session)):
    return await update_category_by_id(session=session, id=id, category_data=category_data)


@router.delete("/{id}", status_code=204)
async def delete_category(id: int, session: AsyncSession = Depends(get_session)):
    await delete_category_by_id(session=session, id=id)


