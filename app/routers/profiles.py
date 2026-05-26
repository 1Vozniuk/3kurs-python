from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.profiles import create_profile, get_profile, list_profiles
from app.db.database import get_db
from app.schemas.profile import ProfileCreate, ProfileOut

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("", response_model=list[ProfileOut])
async def get_profiles(session: AsyncSession = Depends(get_db)) -> list[ProfileOut]:
    return await list_profiles(session)


@router.get("/{profile_id}", response_model=ProfileOut)
async def get_profile_by_id(
    profile_id: int,
    session: AsyncSession = Depends(get_db),
) -> ProfileOut:
    profile = await get_profile(session, profile_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
async def create_profile_item(
    payload: ProfileCreate,
    session: AsyncSession = Depends(get_db),
) -> ProfileOut:
    return await create_profile(session, payload)
