from sqlalchemy.orm import Query
from math import ceil
from starlette.requests import Request
from typing import TypeVar
from typing import Generic
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import func, select


T = TypeVar("T")


class Paginator(BaseModel, Generic[T]):

    current_page: int
    total_pages: int
    count: int
    total: int
    data: list[T]
    next_page: str = None
    prev_page: str = None

    def get_next_page(self) -> int:
        return self.current_page+1 if self.current_page < self.total_pages\
            else self.total_pages

    def get_prev_page(self) -> int:
        return self.current_page-1 if self.current_page > 1 else 1

    def generate_next_page_url(self, request: Request, limit: int):
        self.next_page = "{}{}?page={}&limit={}".format(
            request.url.hostname, request.url.path,
            self.get_next_page(), limit)

    def generate_prev_page_url(self, request: Request, limit: int):
        self.prev_page = "{}{}?page={}&limit={}".format(
            request.url.hostname, request.url.path,
            self.get_prev_page(), limit)

    @classmethod
    async def async_generate_pagination(
            cls,
            async_session: AsyncSession,
            query: Query, page: int,
            limit: int, request: Request,
            no_scalar: bool = False):

        if limit > 100000:
            limit = 100000
        if limit < 5:
            limit = 5

        count_query = select(func.count('*')).select_from(query)
        data = await async_session.execute(count_query)

        total = data.scalar()
        total_pages = ceil(total / limit)

        if page < 1:
            page = 1
        if page > total_pages:
            page = total_pages

        offset = (page-1)*limit
        if offset > 0:
            query = query.offset(offset)

        data: AsyncResult = await async_session.execute(query.limit(limit))
        if no_scalar:
            data = data.all()
        else:
            data = data.scalars().all()
        paginator = cls(
            count=len(data),
            total=total,
            data=data,
            total_pages=total_pages,
            current_page=page)
        paginator.generate_next_page_url(request, limit)
        paginator.generate_prev_page_url(request, limit)

        return paginator