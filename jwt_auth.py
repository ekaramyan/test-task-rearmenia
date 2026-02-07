from jose import JWTError, jwt
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import pbkdf2_sha256
from fastapi.security import OAuth2PasswordBearer
from log import logger
import re

from views.database.users import User
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, HTTPException, status
from database import get_async_db
from config import get_settings
from sqlalchemy.orm import selectinload

config = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pbkdf2_sha256.hash(password)




async def async_get_user(db: AsyncSession, login: str):
    logger.info(f"Username from request: {login}")
    query = (
        select(User)
        .filter(
            User.deleted_at.is_(None),
            or_(
                User.login == login,
                User.phone == login,
            )
        )
        .options(selectinload(User.role))
    )
    result = await db.execute(query)
    user: User | None = result.scalars().first()

    return user


async def async_authenticate_user(db, username: str, password: str) -> User:
    user = await async_get_user(db, username)
    logger.info(f"User from authenticate_user: {user}, {username}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(
        data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.jwt_secret_key,
        algorithm=config.jwt_algorithm)
    return encoded_jwt


def token_decode(token: str):
    return jwt.decode(
        token,
        config.jwt_secret_key,
        algorithms=[config.jwt_algorithm])


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = token_decode(token)
        login: str = payload.get("login")
        type: str = payload.get("type")

        if login is None or type != 'access':
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = await async_get_user(db, login=login)
    if user is None:
        raise credentials_exception
    return user