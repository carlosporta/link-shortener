from pytest import fixture
from httpx import AsyncClient

from app import create_app


@fixture(name="async_client")
async def async_client_fixture():
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
