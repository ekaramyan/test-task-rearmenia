from fastapi import (APIRouter, Depends, HTTPException,
                     Request, Response, status, File, UploadFile)
from controllers.unifided_request import unifided_request, role_secure
from database import get_async_db
from views.database.users import User
from views.json.paginator import Paginator
from views.json.unifided import UnifidedResponse
from views.json.users import UserScheme, UserCreateScheme, UserUpdateScheme
from models.users_logic import AsyncUserService
from sqlalchemy.ext.asyncio import AsyncSession
from jwt_auth import get_current_user
from views.enums.filters import OrderBy, UserFilter


router = APIRouter(prefix='/users', tags=["Users - Пользователи"])


@router.post('', response_model=UnifidedResponse[UserScheme], status_code=201)
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
async def create_user(
        _response: Response,
        data: UserCreateScheme,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    if current_user.role.name not in ["Администратор", "СуперАдмин", "Нейрограф"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough rights to perform this operation"
        )


    async_service = AsyncUserService(db)

    try:
        new_user = await async_service.create(data)
        response_json = await async_service.get(new_user.id)
    except Exception as e:
        await db.close()
        raise e

    return response_json


@router.get('/me', response_model=UnifidedResponse[UserScheme])
@unifided_request
async def get_current_user_info(
        _response: Response,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    async_service = AsyncUserService(db)

    try:
        user = await async_service.get(current_user.id)
        # print(user)
    except Exception as e:
        await db.close()
        raise e

    return user


@router.get('/list', response_model=UnifidedResponse[list[UserScheme]])
@unifided_request
async def get_users_list(
        _response: Response,
        request: Request,
        role_id: int = None,
        search: str = None,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    async_service = AsyncUserService(db)

    try:
        data = await async_service.get_users_list(
            role_id=role_id, search=search)
    except Exception as e:
        await db.close()
        raise e

    return data


@router.get('/{id}', response_model=UnifidedResponse[UserScheme])
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
# НЕ ИСПОЛЬЗУЕТСЯ
async def get_user(
        _response: Response,
        id: int,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    if current_user.role.name not in ["Администратор", "СуперАдмин", "Нейрограф"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough rights to perform this operation"
        )


    async_service = AsyncUserService(db)

    try:
        user = await async_service.get(id)
    except Exception as e:
        await db.close()
        raise e

    return user


@router.delete('/{id}', response_model=UnifidedResponse)
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
async def delete_user(
        _response: Response,
        id: int,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    if current_user.role.name not in ["Администратор", "СуперАдмин", "Нейрограф"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough rights to perform this operation"
        )


    async_service = AsyncUserService(db)

    try:
        await async_service.delete(id)
    except Exception as e:
        await db.close()
        raise e

    return


@router.patch('/me/photo',
              response_model=UnifidedResponse,
              status_code=200)
@unifided_request
async def upload_my_photo(
        _response: Response,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    async_service = AsyncUserService(db)

    try:
        await async_service.upload_file(id=current_user.id,
                                        file=file)
        user = await async_service.get(current_user.id)
    except Exception as e:
        await db.close()
        raise e

    return user


@router.patch('/{id}/photo',
              response_model=UnifidedResponse,
              status_code=200)
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
# НЕ ИСПОЛЬЗУЕТСЯ
async def upload_photo(
        _response: Response,
        id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)): # noqa 117

    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    if current_user.role.name not in ["Администратор", "СуперАдмин", "Нейрограф"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough rights to perform this operation"
        )


    async_service = AsyncUserService(db)

    try:
        await async_service.upload_file(id=id,
                                        file=file)
        user = await async_service.get(id)
    except Exception as e:
        await db.close()
        raise e

    return user


@router.patch('/{id}', response_model=UnifidedResponse[UserScheme])
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
async def update_user(
        _response: Response,
        id: int,
        data: UserUpdateScheme,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    if current_user.role.name not in ["Администратор", "СуперАдмин", "Нейрограф"] and current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have enough rights to perform this operation')

    async_service = AsyncUserService(db)

    try:
        await async_service.update(id, data)
        response_json = await async_service.get(id)
    except Exception as e:
        await db.close()
        raise e

    return response_json


@router.get('', response_model=UnifidedResponse[Paginator[UserScheme]])
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
async def get_users(
        _response: Response,
        request: Request,
        limit: int = 25,
        page: int = 1,
        role_id: int = None,
        order_by: OrderBy = OrderBy.DESC,
        parameter: UserFilter = UserFilter.ID,
        search: str = None,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    if current_user.role.name not in ["Администратор", "СуперАдмин", "Нейрограф"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough rights to perform this operation"
        )


    async_service = AsyncUserService(db)

    try:
        pagination = await async_service.get_list(
            request=request,
            limit=limit,
            page=page,
            role_id=role_id,
            order_by=order_by,
            parameter=parameter,
            search=search)
    except Exception as e:
        await db.close()
        raise e

    return pagination
