import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from database_test import get_async_db as test_async_db
from database_test import engine, Base
from database import get_async_db


from controllers.auth import router

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_async_db] = test_async_db
client = TestClient(app)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def drop_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def setup_module(module):

    # asyncio.run(init_models())
    pass


def teardown_module(module):

    pass


def test__api_works():
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test__generate_token_422_error():
    response = client.post("/auth/token")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test__generate_token_401_error():
    response = client.post("/auth/token", data={
        "username": "admin", "password": "Qwerty"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test__generate_token_200_success():
    response = client.post("/auth/token", data={
        "username": "admin", "password": "Qwerty123"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test__generate_and_refresh_token_200_success():
    response = client.post("/auth/token", data={
        "username": "admin", "password": "Qwerty123"})
    assert response.status_code == 200
    response_refresh = client.post("/auth/refresh", data={"refresh_token": response.json().refresh_token})
    assert response.response_refresh == 200
