from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.crud.users import create_user, get_user_by_email
from app.db.database import get_db
from app.schemas.user import UserLogin, UserOut, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserRegister,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    existing = await get_user_by_email(session, payload.email)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    hashed_password = hash_password(payload.password)
    user = await create_user(session, payload, hashed_password)
    return user


@router.post("/login")
async def login_user(
    payload: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_db),
) -> dict:
    user = await get_user_by_email(session, payload.email)
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return {"access_token": token}


@router.post("/logout")
async def logout_user(response: Response) -> dict:
    response.delete_cookie("access_token")
    return {"status": "logged_out"}
