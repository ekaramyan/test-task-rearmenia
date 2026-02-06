from asyncio import gather
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, select, desc, asc, or_, func
from views.database.roles import Role
from views.database.users import User
from views.json.paginator import Paginator
from views.json.users import UserCreateScheme, UserScheme, UserUpdateScheme
from fastapi import HTTPException, Request, status, File, UploadFile
from sqlalchemy.orm import selectinload
from passlib.hash import pbkdf2_sha256
import os
import aiofiles
from config import UPLOAD_PATH
from .roles__logic import AsyncRoleService
from views.enums.filters import OrderBy, UserFilter


class AsyncUserService():

    def __init__(self, session: AsyncSession):
        self.session = session

    async def auto_create_admin(self):

        query = select(User).where(User.login == 'admin')
        result = await self.session.execute(query)
        elem: User | None = result.scalars().first()
        if elem:
            return

        role = Role(name="Администратор")
        try:
            self.session.add(role)
            await self.session.flush()
            await self.session.refresh(role)
            print(role.id)
        except Exception as e:
            print(e)
            await self.session.rollback()
            await self.session.close()
            return

        admin_data = UserCreateScheme(
            first_name='Admin',
            last_name='Admin',
            email='admin@mail.ru',
            login='admin',
            password='1234',
            role_id=role.id
        )

        await self.create(admin_data)

    async def get(self, id: int) -> UserScheme:

        query = select(User).where(User.deleted_at.is_(None)).where(User.id == id)\
            .options(selectinload(User.role))

        result = await self.session.execute(query)
        elem: User | None = result.scalars().first()

        if elem is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        json_response = elem.json_scheme()

        return json_response

    async def __is_user_already_exists_by(self, column: Column, value) -> bool:

        query = select(User).where(User.deleted_at.is_(None)).where(column == value)
        result = await self.session.execute(query)
        elem: User | None = result.scalars().first()

        return elem is not None

    async def create(self, data: UserCreateScheme) -> User:

        is_email_exists, is_login_exists = await gather(
            self.__is_user_already_exists_by(User.email, data.email),
            self.__is_user_already_exists_by(User.login, data.login))

        if is_email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email address already exists")

        if is_login_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This login already exists")

        role_service = AsyncRoleService(self.session)
        role = await role_service.get(data.role_id)
        data.password = pbkdf2_sha256.hash(data.password)
        new_user = User(**data.dict())

        try:
            self.session.add(new_user)
            await self.session.flush([new_user])

        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to save changes")
        await self.session.commit()

        return new_user

    async def delete(self, id: int):

        user = await self.session.get(User, id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")
        try:
            user.deleted_at = datetime.utcnow()
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to save changes")

    async def update(self, id: int, data: UserUpdateScheme) -> User:

        user = await self.session.get(User, id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        role_service = AsyncRoleService(self.session)

        user.role_id = data.role_id

        user.first_name = data.first_name or user.first_name
        user.last_name = data.last_name or user.last_name

        if data.email:
            is_email_exists = await self.__is_user_already_exists_by(
                column=User.email,
                value=data.email)
            if is_email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email address already exists")

        if data.login:
            is_login_exists = await self.__is_user_already_exists_by(
                column=User.login,
                value=data.login)
            if is_login_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This login already exists")

        user.email = data.email or user.email
        user.login = data.login or user.login
        user.phone = data.phone or user.phone
        user.tg = data.tg or user.tg

        if data.password:
            user.password = pbkdf2_sha256.hash(data.password)

        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to save changes:"+str(e))

        return

    async def get_list(
            self,
            request: Request,
            limit: int = 25,
            page: int = 1,
            role_id: int = None,
            order_by: OrderBy = OrderBy.DESC,
            parameter: UserFilter = UserFilter.ID,
            search: str = None) -> Paginator[UserScheme]:

        query = select(User).where(
            User.deleted_at.is_(None)
        ).options(selectinload(User.role))

        if search:
            query = query.where(
                func.lower(User.login).like(
                 "%{0}%".format(search.lower())))

        filter_way = asc if order_by == OrderBy.ASC else desc

        match(parameter):
            case UserFilter.FIRST_NAME:
                query = query.order_by(filter_way(User.first_name))
            case UserFilter.L_NAME:
                query = query.order_by(filter_way(User.last_name))
            case UserFilter.PHONE:
                query = query.order_by(filter_way(User.phone))
            case UserFilter.TG:
                query = query.order_by(filter_way(User.tg))
            case UserFilter.EMAIL:
                query = query.order_by(filter_way(User.email))
            case _:
                query = query.order_by(filter_way(User.id))

        if role_id:
            query = query.where(User.role_id == role_id)

        paginator = await Paginator.async_generate_pagination(
            self.session, query, page,
            limit, request)
        paginator.data = [i.json_scheme() for i in paginator.data]

        return paginator

    async def get_users_list(
            self,
            role_id: int = None,
            search: str = None) -> list[UserScheme]:

        query = select(User).where(
            User.deleted_at.is_(None)
        ).options(selectinload(User.role))

        if role_id:
            query = query.where(User.role_id == role_id)

        if search:
            query = query.where(
                or_(
                    func.lower(User.first_name).like(
                        '%{0}%'.format(search.lower())),
                    func.lower(User.last_name).like(
                        '%{0}%'.format(search.lower())),
                    func.lower(User.email).like(
                        '%{0}%'.format(search.lower())),
                    func.lower(User.login).like(
                        '%{0}%'.format(search.lower())),
                    User.phone.like('%{0}%'.format(search))
                )
            )

        users = await self.session.execute(query)

        users_list = list()

        for item in users:
            item: User = item[0]
            users_list.append(item.json_scheme())

        return users_list

    async def upload_file(
            self, id: int,
            file: UploadFile = File(...)):

        user = await self.session.get(User, id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        new_filename = "user_{}.{}".format(
            str(id), file.filename.split('.')[-1])
        new_filename = os.path.join("users", new_filename)
        SAVE_PATH_FILE = os.path.join(UPLOAD_PATH, new_filename)
        async with aiofiles.open(SAVE_PATH_FILE, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write

        user.photo = new_filename

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to save changes")

        return
