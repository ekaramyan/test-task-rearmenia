from fastapi import APIRouter, Depends, Request, Response
from controllers.unifided_request import unifided_request, role_secure
from database import get_async_db
from views.database.users import User
from views.json.paginator import Paginator
from views.json.unifided import UnifidedResponse
from views.json.roles import RoleCreateScheme, \
    RoleScheme, RoleUpdateScheme
from models.roles__logic import AsyncRoleService
from sqlalchemy.ext.asyncio import AsyncSession
from jwt_auth import get_current_user


router = APIRouter(prefix='/roles',
                   tags=["Role - Роль пользователя"])


@router.post('', response_model=UnifidedResponse[RoleScheme], status_code=201)
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
# НЕ ИСПОЛЬЗУЕТСЯ
async def create_role(
        _response: Response,
        data: RoleCreateScheme,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    async_service = AsyncRoleService(db)

    try:
        new_role = await async_service.create(data)
        response_json = await async_service.get(new_role.id)
    except Exception as e:
        raise e

    return response_json


@router.get('/{id}', response_model=UnifidedResponse[RoleScheme],
            status_code=200)
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
# НЕ ИСПОЛЬЗУЕТСЯ
async def get_role(
        _response: Response,
        id: int,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    async_service = AsyncRoleService(db)

    try:
        role = await async_service.get(id)
    except Exception as e:
        await db.close()
        raise e

    return role


@router.delete('/{id}',  response_model=UnifidedResponse)
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
# НЕ ИСПОЛЬЗУЕТСЯ
async def delete_role(
        _response: Response,
        id: int,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    async_service = AsyncRoleService(db)

    try:
        await async_service.delete(id)
    except Exception as e:
        await db.close()
        raise e

    return


@router.patch('/{id}', response_model=UnifidedResponse[RoleScheme],
              status_code=200)
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
# НЕ ИСПОЛЬЗУЕТСЯ
async def update_role(
        _response: Response,
        id: int,
        data: RoleUpdateScheme,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    async_service = AsyncRoleService(db)

    try:
        role = await async_service.update(id, data)
        response_json = await async_service.get(role.id)
    except Exception as e:
        await db.close()
        raise e

    return response_json


@router.get('', response_model=UnifidedResponse[Paginator[RoleScheme]])
@unifided_request
@role_secure(roles=["Администратор", "СуперАдмин", "Нейрограф"])  # noqa 501
async def get_all_role(
        _response: Response,
        request: Request,
        limit: int = 25,
        page: int = 1,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)):

    async_service = AsyncRoleService(db)

    try:
        pagination = await async_service.get_list(
            request=request,
            limit=limit,
            page=page)
    except Exception as e:
        await db.close()
        raise e

    return pagination
