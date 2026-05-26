from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Order
from app.schemas.order import OrderCreate


async def create_order(session: AsyncSession, payload: OrderCreate) -> Order:
    order = Order(**payload.model_dump())
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def list_orders(session: AsyncSession) -> list[Order]:
    result = await session.execute(select(Order))
    return list(result.scalars().all())


async def list_orders_for_user(session: AsyncSession, user_id: int) -> list[Order]:
    result = await session.execute(select(Order).where(Order.user_id == user_id))
    return list(result.scalars().all())


async def get_order(session: AsyncSession, order_id: int) -> Order | None:
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()
