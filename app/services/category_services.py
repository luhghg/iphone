from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.category_repository import create_category, get_all_categories, get_category_by_id, get_category_by_slug, update_category, delete_category
from app.schemas.category_schemas import CategoryCreate, CategoryUpdate
from app.models.bd_models import Category



async def create_new_category(session: AsyncSession, category_data: CategoryCreate) -> Category:
    if await get_category_by_slug(session=session, slug=category_data.slug):
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    return await create_category(session=session, category_data=category_data)


async def get_categories(session:AsyncSession) -> list[Category]:
    return await get_all_categories(session=session)


async def get_category(session:AsyncSession, id:int) -> Category:
    if category := await get_category_by_id(session=session, id=id):
        return category
    raise HTTPException(status_code=404, detail="Category not found")


async def update_category_by_id(session : AsyncSession, id: int, category_data: CategoryUpdate) -> Category:
    category = await get_category_by_id(session=session, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category_data.slug and await get_category_by_slug(session=session, slug=category_data.slug):
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    return await update_category(session=session, category=category, category_data=category_data)


async def delete_category_by_id(session: AsyncSession, id: int) -> None:
    category = await get_category_by_id(session=session, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await delete_category(session=session, category=category)



