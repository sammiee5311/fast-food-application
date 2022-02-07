import pytest
from fastapi import status
from httpx import AsyncClient
from main import HOST, PORT, app

URL = f"http://{HOST}:{PORT}"


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "This server is an api for id generator."}


@pytest.mark.anyio
async def test_get_id():
    async with AsyncClient(app=app, base_url=URL) as ac:
        response = await ac.get("/id/")
        assert response.status_code == status.HTTP_200_OK
        assert "uuid" in response.json()
