from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category, Order, Product, Profile, User


async def seed_data(session: AsyncSession) -> None:
    existing = await session.execute(select(User).limit(1))
    if existing.scalar_one_or_none() is not None:
        return

    user_1 = User(name="Ivan Petrenko", email="ivan@example.com")
    user_2 = User(name="Olena Kovalenko", email="olena@example.com")

    profile_1 = Profile(user=user_1, bio="Backend developer", phone="+380000000001")
    profile_2 = Profile(user=user_2, bio="Product manager", phone="+380000000002")

    category_1 = Category(name="Electronics")
    category_2 = Category(name="Books")

    product_1 = Product(name="Laptop", price=Decimal("1200.00"), category=category_1)
    product_2 = Product(name="E-Reader", price=Decimal("150.00"), category=category_1)
    product_3 = Product(name="Clean Architecture", price=Decimal("45.00"), category=category_2)

    order_1 = Order(user=user_1, product=product_1, quantity=1, status="new")
    order_2 = Order(user=user_2, product=product_3, quantity=2, status="paid")

    session.add_all(
        [
            user_1,
            user_2,
            profile_1,
            profile_2,
            category_1,
            category_2,
            product_1,
            product_2,
            product_3,
            order_1,
            order_2,
        ]
    )
    await session.commit()
