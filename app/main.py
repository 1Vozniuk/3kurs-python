from fastapi import FastAPI

from app.routers.users import router as users_router

app = FastAPI(title="FastAPI Lab 3")

app.include_router(users_router)


@app.get("/")
def root() -> dict:
    return {"status": "ok"}