import pytest
from httpx import AsyncClient

PREFIX = "/hello"


@pytest.mark.anyio
class TestHello:

    async def test_get(self, client: AsyncClient):
        url = f"{PREFIX}/get"
        response = await client.get(url)
        assert response.text.lower() == "hello!"
