import asyncio

import pytest
from httpx import AsyncClient

from app.main import app

URL = 'http://web:8000'


@pytest.fixture()
async def async_client() -> AsyncClient:  # type: ignore
    async with AsyncClient(app=app, base_url=URL) as client:
        yield client
        await client.aclose()


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
