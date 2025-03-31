import requests

API_BASE_URL = "http://127.0.0.1:8000"


# Get
def test_ping():
    url = f"{API_BASE_URL}/ping"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_naive_tsp():
    url = f"{API_BASE_URL}/naive_tsp"
    response = requests.get(
        url,
        json={
            "start": {"coordinates": [121.0, 14.6]},
            "other_points": [{"coordinates": [121.01, 14.61]}],
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {"coordinates": [121.0, 14.6]},
        {"coordinates": [121.01, 14.61]},
        {"coordinates": [121.0, 14.6]},
    ]


def test_login_valid():
    url = f"{API_BASE_URL}/login"
    response = requests.post(
        url, json={"username": "Constituent1", "password": "Constituent1"}
    )

    assert response.status_code == 200
    assert response.json() == {"person_id": 1, "access_control": 1}


def test_login_invalid():
    url = f"{API_BASE_URL}/login"
    response = requests.post(
        url,
        json={
            "username": "UserNameThatIsNotInDatabase",
            "password": "PasswordThatIsNotInDatabase",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"person_id": 0, "access_control": 0}


def test_convert_coordinates():
    url = f"{API_BASE_URL}/convert_coordinates"
    response = requests.post(
        url,
        json=[
            {"coordinates": [121.06846773745589, 14.648772127025484]},
            {"coordinates": [121.05786349512705, 14.643245228663027]},
        ],
    )

    assert response.status_code == 200
    assert response.json() == {
        "locations": [
            "J3X9+G94, P. Velasquez Street, Diliman, Quezon City, 1800 Metro Manila, Philippines",
            "41-B Mapagkawanggawa, Diliman, Lungsod Quezon, 1101 Kalakhang Maynila, Philippines",
        ]
    }


def test_test():
    url = f"{API_BASE_URL}/test"
    response = requests.get(url)
    assert response.status_code == 200


# Post
def test_tsp():
    url = f"{API_BASE_URL}/tsp"
    response = requests.post(
        url,
        json={
            "start": {"coordinates": [121.0, 14.6]},
            "other_points": [{"coordinates": [121.01, 14.61]}],
        },
    )

    assert response.status_code == 200
    response_data = response.json()

    # Check basic structure of response because of lengthy output
    assert isinstance(response_data, list)
    assert "start" in response_data[0]
    assert "end" in response_data[0]
    assert "data" in response_data[0]
    assert "route" in response_data[0]["data"]
    assert "geojson" in response_data[0]["data"]
    assert response_data[0]["data"]["message"] == "Safe route found."


def test_directions():
    url = f"{API_BASE_URL}/directions"
    response = requests.post(
        url,
        json={
            "start": "121.06860972815775,14.649881813121752",
            "end": "121.06878977849078,14.649391333636387",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "route": {"duration": 0.5311600511633648, "distanceKm": 0.04426333759694707},
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [121.0686508, 14.6497608],
                            [121.0686546, 14.6497514],
                            [121.0686964, 14.6496477],
                            [121.0688009, 14.6493884],
                        ],
                    },
                    "properties": {},
                }
            ],
        },
        "message": "Safe route found.",
    }


def test_checkCoordinates():
    url = f"{API_BASE_URL}/checkCoordinates"
    response = requests.post(
        url, json={"coordinates": [121.05959688150006, 14.590127718074672]}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "true"}


def test_add_request():
    url = f"{API_BASE_URL}/add_request"
    response = requests.post(
        url,
        json={
            "person_id": 3,
            "coordinates": [
                {"coordinates": ["121.0694063", "14.65679956"]},
                {"coordinates": ["121.0411614", "14.66310851"]},
                {"coordinates": ["121.0219046", "14.65919254"]},
                {"coordinates": ["121.0177288", "14.65537632"]},
            ],
        },
    )

    assert response.status_code == 200
    assert "request_id" in response.json()


def test_get_route_info():
    url = f"{API_BASE_URL}/get_route_info"
    response = requests.post(url, json={"route_id": 96})

    assert response.status_code == 200
    assert "payload" in response.json()


def test_save_route():
    url = f"{API_BASE_URL}/save_route"
    response = requests.post(
        url,
        json={
            "request_id": 154,
            "points": {
                "start": {"coordinates": [121.04932, 14.65491]},
                "other_points": [{"coordinates": [121.07471, 14.66651]}],
            },
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_update_rescued():
    url = f"{API_BASE_URL}/update_rescued"
    response = requests.post(url, json={"request_id": 0})

    assert response.status_code == 200
    assert response.json() == {"message": "done"}


def test_update_ongoing():
    url = f"{API_BASE_URL}/update_ongoing"
    response = requests.post(url, json={"request_id": 1})

    assert response.status_code == 200
    assert response.json() == {"message": "done"}


def test_get_rescuers():
    url = f"{API_BASE_URL}/get_rescuers"
    response = requests.post(
        url,
    )

    assert response.status_code == 200
    assert response.json() == {
        "rescuers": [
            {"person_id": 2, "username": "Rescuer1"},
            {"person_id": 4, "username": "Rescuer2"},
            {"person_id": 5, "username": "Rescuer3"},
        ]
    }


def test_assign():
    url = f"{API_BASE_URL}/assign"
    response = requests.post(url, json={"request_id": 1, "rescuer_id": 2})

    assert response.status_code == 200


def test_compare_coordinates():
    url = f"{API_BASE_URL}/compare_coordinates"
    response = requests.post(
        url,
        json={
            "person_id": 3,
            "coordinates": [
                {"coordinates": [121.06211566207924, 14.646743398830466]},
                {"coordinates": [121.06210078349255, 14.646615760409261]},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "true"}

    response = requests.post(
        url,
        json={
            "person_id": 3,
            "coordinates": [
                {"coordinates": [121.06211326644774, 14.6466919912408]},
                {"coordinates": [121.06210068276675, 14.646621999279489]},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "false"}
