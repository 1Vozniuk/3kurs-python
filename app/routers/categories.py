from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.categories import create_category, get_category, list_categories
from app.db.database import get_db
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
async def get_categories(session: AsyncSession = Depends(get_db)) -> list[CategoryOut]:
    return await list_categories(session)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(get_db),
) -> CategoryOut:
    category = await get_category(session, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category_item(
    payload: CategoryCreate,
    session: AsyncSession = Depends(get_db),
) -> CategoryOut:
    return await create_category(session, payload)
