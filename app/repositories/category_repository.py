from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bd_models import Category
from app.schemas.category_schemas import CategoryCreate, CategoryUpdate
from sqlalchemy import select

async def create_category(session: AsyncSession, category_data: CategoryCreate) -> Category:
    category = Category(name=category_data.name, slug=category_data.slug)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def get_all_categories(session: AsyncSession) -> list[Category]:
    query = (
        select(Category)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_category_by_id(session:AsyncSession, id: int) -> Category:
    query = (
        select(Category)
        .where(Category.id == id)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_category_by_slug(session: AsyncSession, slug: str) -> Category:
    query = (
        select(Category)
        .where(Category.slug == slug)
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_category(session: AsyncSession, category: Category, category_data: CategoryUpdate) -> Category:
    if category_data.name is not None:
        category.name = category_data.name
    if category_data.slug is not None:
        category.slug = category_data.slug

    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def delete_category(session: AsyncSession, category: Category) -> None:
    await session.delete(category)
    await session.commit()

    



