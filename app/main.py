from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import async_session
from app.db.seed import seed_data
from app.routers.categories import router as categories_router
from app.routers.orders import router as orders_router
from app.routers.profiles import router as profiles_router
from app.routers.products import router as products_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with async_session() as session:
        await seed_data(session)
    yield


app = FastAPI(title="FastAPI Lab 4", lifespan=lifespan)

app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
def root() -> dict:
    return {"status": "ok"}