import requests

API_BASE_URL = "http://127.0.0.1:8000"

def test_ping():
    url = f"{API_BASE_URL}/ping"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}