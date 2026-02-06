from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, select
from views.database.roles import Role
from views.json.paginator import Paginator
from views.json.roles import RoleScheme, RoleCreateScheme, RoleUpdateScheme # noqa 501
from fastapi import HTTPException, Request, status


class AsyncRoleService():

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> RoleScheme:

        query = select(Role).where(Role.id == id)

        result = await self.session.execute(query)
        elem: Role | None = result.scalars().first()

        if elem is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found")

        json_response = elem.json_scheme()

        return json_response

    async def __is_role_already_exists_by(self, column: Column, value) -> bool: # noqa 501

        query = select(Role).where(column == value)
        result = await self.session.execute(query)
        elem: Role | None = result.scalars().first()

        return elem is not None

    async def create(self, data: RoleCreateScheme) -> Role:  # noqa 501

        is_name_exists = await self.__is_role_already_exists_by(Role.name, data.name) # noqa 501

        if is_name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This name already exists")

        new_role = Role(**data.dict())

        try:
            self.session.add(new_role)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to save changes")

        return new_role

    async def delete(self, id: int):

        role = await self.session.get(Role, id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found")
        try:
            await self.session.delete(role)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to save changes")

    async def update(self, id: int, data: RoleUpdateScheme) -> Role: # noqa 501

        role = await self.session.get(Role, id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found")

        if data.name:
            is_name_exists = await self.__is_role_already_exists_by(column=Role.name, value=data.name) # noqa 501
            if is_name_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This name exists")

        role.name = data.name or role.name
        role.role_value = data.role_value or role.role_value

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to save changes")

        return role

    async def get_list(
            self,
            request: Request,
            limit: int = 25,
            page: int = 1) -> Paginator[RoleScheme]:

        query = select(Role)

        paginator = await Paginator.async_generate_pagination(
            self.session, query, page,
            limit, request)
        paginator.data = [i.json_scheme() for i in paginator.data]

        return paginator
