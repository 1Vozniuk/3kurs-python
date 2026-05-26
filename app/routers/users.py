from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import create_user, get_user, list_users
from app.db.database import get_db
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
async def get_users(session: AsyncSession = Depends(get_db)) -> list[UserOut]:
    return await list_users(session)


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_item(
    payload: UserCreate,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    return await create_user(session, payload)
