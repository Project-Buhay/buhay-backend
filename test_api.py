import requests

from db_env import API_BASE_URL

def test_ping():
    url = f"{API_BASE_URL}/ping"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}