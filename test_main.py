import pytest
import warnings
from fastapi import status
from main import app, startup_event
import json
from fastapi.testclient import TestClient
import asyncpg
from db_env import DB_CACHE_URL

VALID_START = "121.04932,14.65491"
VALID_END = "121.07471,14.66651"


# Database connection fixture
@pytest.fixture(scope="module")
async def db_connection():
    # Create a connection pool for the test database
    pool = await asyncpg.create_pool(dsn=DB_CACHE_URL)
    yield pool  # Provide the connection pool to the tests
    await pool.close()  # Close the pool after tests are done


@pytest.fixture(scope="module")
def client(db_connection):
    # Use the TestClient with the FastAPI app
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_invalid_start_end_coordinates(client):
    # Test invalid start and end coordinates
    async with startup_event(app):
        body = {"start": "invalid_coords", "end": "invalid_coords"}

        response = client.post("/directions", json=body)
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        )  # Expecting a bad request for invalid coordinates


@pytest.mark.asyncio
async def test_missing_start_parameter(client):
    # Test missing start parameter
    async with startup_event(app):
        body = {"end": VALID_END}

        response = client.post("/directions", json=body)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_missing_end_parameter(client):
    # Test missing end parameter
    async with startup_event(app):
        body = {"start": VALID_START}

        response = client.post("/directions", json=body)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        )  # Expecting a bad request for missing end
