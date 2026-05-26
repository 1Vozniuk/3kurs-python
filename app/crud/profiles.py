from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Profile
from app.schemas.profile import ProfileCreate


async def create_profile(session: AsyncSession, payload: ProfileCreate) -> Profile:
    profile = Profile(**payload.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def list_profiles(session: AsyncSession) -> list[Profile]:
    result = await session.execute(select(Profile))
    return list(result.scalars().all())


async def get_profile(session: AsyncSession, profile_id: int) -> Profile | None:
    result = await session.execute(select(Profile).where(Profile.id == profile_id))
    return result.scalar_one_or_none()
