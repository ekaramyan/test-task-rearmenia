from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from log import logger
from database import get_async_db
from jwt_auth import (
    async_authenticate_user,
    create_access_token,
    token_decode)
from config import get_settings
from views.database.users import User
from views.json.auth import AuthScheme, RefreshScheme
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=["Auth - Авторизация"])
config = get_settings()
# НЕ ИСПОЛЬЗУЕТСЯ

def generate_jwt_tokens(login: str):

    access_token_expires = timedelta(
        minutes=config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"login": login, 'type': "access"},
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(
        minutes=config.refresh_token_expire_minutes)
    refresh_token = create_access_token(
        data={"login": login, 'type': 'refresh'},
        expires_delta=refresh_token_expires)

    auth = AuthScheme(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer")
    return auth


@router.post(
        path="/token",
        response_model=AuthScheme,
        name="Авторизация пользователя")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_db)):
    logger.info(f"Attempt to login: {form_data.username}")

    user: User = await async_authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    logger.info(f"Username login from DB: {user.login}")
    auth = generate_jwt_tokens(user.login)
    return auth


@router.post(
        path='/refresh',
        response_model=AuthScheme,
        name="Обновление токенов пользователя")
async def refresh_token(token: RefreshScheme):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = token_decode(token.refresh_token)
        login: str = payload.get("login")
        type: str = payload.get("type")

        if login is None or type != 'refresh':
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    auth = generate_jwt_tokens(login)

    return auth

