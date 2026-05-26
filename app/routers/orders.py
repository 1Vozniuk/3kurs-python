from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.orders import create_order, get_order, list_orders
from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderOut])
async def get_orders(session: AsyncSession = Depends(get_db)) -> list[OrderOut]:
    return await list_orders(session)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(get_db),
) -> OrderOut:
    order = await get_order(session, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_item(
    payload: OrderCreate,
    session: AsyncSession = Depends(get_db),
) -> OrderOut:
    return await create_order(session, payload)
