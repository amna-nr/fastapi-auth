from app.services.auth import register, login, refresh, logout
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.database import db_dependency

from fastapi import APIRouter, Cookie


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register")
async def register_user(credentials: RegisterRequest, db: db_dependency):
    return await register(credentials, db)

@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: LoginRequest, db: db_dependency):
    return await login(credentials, db)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(db: db_dependency, refresh_token: str = Cookie(...)):
    return await refresh(db, refresh_token)

@router.post("/logout")
async def logout_user(refresh_token: str = Cookie(...)):
    return await logout(refresh_token) 