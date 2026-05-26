from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.products import create_product, get_product, list_products
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
async def get_products(session: AsyncSession = Depends(get_db)) -> list[ProductOut]:
    return await list_products(session)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(get_db),
) -> ProductOut:
    product = await get_product(session, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product_item(
    payload: ProductCreate,
    session: AsyncSession = Depends(get_db),
) -> ProductOut:
    return await create_product(session, payload)
