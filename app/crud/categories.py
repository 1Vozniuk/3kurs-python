from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category
from app.schemas.category import CategoryCreate


async def create_category(session: AsyncSession, payload: CategoryCreate) -> Category:
    category = Category(**payload.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def list_categories(session: AsyncSession) -> list[Category]:
    result = await session.execute(select(Category))
    return list(result.scalars().all())


async def get_category(session: AsyncSession, category_id: int) -> Category | None:
    result = await session.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()
