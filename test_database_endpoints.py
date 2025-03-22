import pytest
from pprint import pprint

from httpx import ASGITransport, AsyncClient
from main import app, startup_event

@pytest.mark.asyncio
async def test_login_valid():
    async with startup_event(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            request = client.build_request(url="/login", method="POST", json={
                "username": "Constituent1",
                "password": "Constituent1"
            })
            response = await client.send(request)

            pprint(response.json())
            assert response.json() == {
                "person_id": 1,
                "access_control": 1
            }

@pytest.mark.asyncio
async def test_login_invalid():
    async with startup_event(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            request = client.build_request(url="/login", method="POST", json={
                "username": "UserNameThatIsNotInDatabase",
                "password": "PasswordThatIsNotInDatabase"
            })
            response = await client.send(request)

            pprint(response.json())
            assert response.json() == {
                "person_id": 0,
                "access_control": 0
            }

@pytest.mark.asyncio
async def test_convert_coordinates():
    async with startup_event(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            request = client.build_request(url="/convert_coordinates", method="POST", json=[
                {
                    "coordinates": [
                        121.06846773745589,
                        14.648772127025484
                ]
                },
                {
                    "coordinates":[
                        121.05786349512705,
                        14.643245228663027
                    ]
                }
            ])

            response = await client.send(request)

            pprint(response.json())
            assert response.json() == {
                "locations": [
                    "University of the Philippines Alumni Engineers' Centennial Hall, P. Velasquez Street, Diliman, Quezon City, 1800 Metro Manila, Philippines",
                    "41-B Mapagkawanggawa, Diliman, Lungsod Quezon, 1101 Kalakhang Maynila, Philippines"
                ]
            }