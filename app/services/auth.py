from app.core.security import hash_password, check_password, generate_access_token, generate_refresh_token
from app.core.database import db_dependency
from app.schemas.auth import RegisterRequest, LoginRequest
from app.models.user import User
from app.core.redis import redis_client
from app.core.config import settings

from fastapi import HTTPException, Cookie
from starlette import status
from sqlalchemy import select
from uuid import UUID


async def register(credentials: RegisterRequest, db: db_dependency):
    
    if credentials.password != credentials.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Passwords don't match." 
        )
    
    result = await db.execute(select(User).where(User.email == credentials.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already in use." 
        )

    password_hash = hash_password(credentials.password)

    new_user = User(email=credentials.email, password_hash=password_hash)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message" : "User has been created."}


async def login(credentials: LoginRequest, db: db_dependency):
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )
    
    if not check_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
            )
    
    access_token = generate_access_token({"id" :  str(user.id), "sub" : user.email})
    refresh_token = generate_refresh_token()

    await redis_client.set(
        f"refresh:{refresh_token}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRES_DAYS * 86400
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer",
        "refresh_token" : refresh_token
    }


async def refresh(db: db_dependency, refresh_token: str = Cookie(...)):
    user_id = await redis_client.get(f"refresh:{refresh_token}")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )
    
    access_token = generate_access_token({"id" : str(user.id), "sub" : user.email})

    await redis_client.delete(f"refresh:{refresh_token}")

    refresh_token = generate_refresh_token()
    
    await redis_client.set(
        f"refresh:{refresh_token}",
        str(user.id),
        ex=settings.REFRESH_TOKEN_EXPIRES_DAYS * 86400
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer",
        "refresh_token" : refresh_token
    }


async def logout(refresh_token: str = Cookie(...)):
    user_id = await redis_client.get(f"refresh:{refresh_token}")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired refresh token"
        )
        
    await redis_client.delete(f"refresh:{refresh_token}")

    return {"message" : "You have been logged out"}
