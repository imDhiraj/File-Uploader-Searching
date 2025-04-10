# tests/conftest.py
import pytest_asyncio
from httpx import AsyncClient
from main import app
from fastapi import FastAPI
from httpx import ASGITransport

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
