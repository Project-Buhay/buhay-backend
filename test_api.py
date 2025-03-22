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
            "start": {
                "coordinates": [121.0, 14.6]
            },
            "other_points": [
                {
                    "coordinates": [121.01, 14.61]
                }
            ]
        }
    )

    assert response.status_code == 200
    assert response.json() == [{
            "coordinates": [
                121.0,
                14.6
            ]
        },
        {
            "coordinates": [
                121.01,
                14.61
            ]
        },
        {
            "coordinates": [
                121.0,
                14.6
            ]
        }
    ]

def test_login():
    url = f"{API_BASE_URL}/login"
    response = requests.post(
        url,
        json={
            "username": "Constituent1",
            "password": "Constituent1"
        }
    )

    assert response.status_code == 200

def test_convert_coordinates():
    url = f"{API_BASE_URL}/convert_coordinates"
    response = requests.post(
        url,
        json=[
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
        ]
    )

    assert response.status_code == 200
    assert response.json() == {
        "locations": [
            "University of the Philippines Alumni Engineers' Centennial Hall, P. Velasquez Street, Diliman, Quezon City, 1800 Metro Manila, Philippines",
            "41-B Mapagkawanggawa, Diliman, Lungsod Quezon, 1101 Kalakhang Maynila, Philippines"
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
            "start": {
                "coordinates": [121.0, 14.6]
            },
            "other_points": [
                {
                    "coordinates": [121.01, 14.61]
                }
            ]
        }
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
        "start": "121.0000,14.6000",
        "end": "121.0100,14.6100"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "route": {
            "duration": 26.764869155748308,
            "distanceKm": 2.2304057629790255
        },
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [
                                120.9999984,
                                14.6000936
                            ],
                            [
                                120.999976,
                                14.6001394
                            ],
                            [
                                120.9997433,
                                14.6006017
                            ],
                            [
                                120.9998838,
                                14.6009801
                            ],
                            [
                                121.0002797,
                                14.6011276
                            ],
                            [
                                121.000241,
                                14.6012973
                            ],
                            [
                                121.0003164,
                                14.6013161
                            ],
                            [
                                121.0000639,
                                14.6019499
                            ],
                            [
                                121.0000042,
                                14.6020914
                            ],
                            [
                                120.9998164,
                                14.6025361
                            ],
                            [
                                120.9995841,
                                14.6030864
                            ],
                            [
                                120.9995283,
                                14.6032118
                            ],
                            [
                                120.9993526,
                                14.6036345
                            ],
                            [
                                120.9993474,
                                14.6036471
                            ],
                            [
                                120.9990092,
                                14.6044287
                            ],
                            [
                                120.9996481,
                                14.6047346
                            ],
                            [
                                120.9996839,
                                14.6047549
                            ],
                            [
                                120.9999917,
                                14.6049827
                            ],
                            [
                                121.0001273,
                                14.6050848
                            ],
                            [
                                121.0002943,
                                14.6052107
                            ],
                            [
                                121.0004507,
                                14.6053215
                            ],
                            [
                                121.0005982,
                                14.6054237
                            ],
                            [
                                121.000923,
                                14.6056237
                            ],
                            [
                                121.0012412,
                                14.6058068
                            ],
                            [
                                121.0015536,
                                14.6059999
                            ],
                            [
                                121.0019184,
                                14.606227
                            ],
                            [
                                121.0022021,
                                14.6063844
                            ],
                            [
                                121.0025352,
                                14.6065673
                            ],
                            [
                                121.0028585,
                                14.6067813
                            ],
                            [
                                121.0030653,
                                14.6069091
                            ],
                            [
                                121.0031506,
                                14.6069672
                            ],
                            [
                                121.0034004,
                                14.6072591
                            ],
                            [
                                121.0041455,
                                14.6066866
                            ],
                            [
                                121.0043731,
                                14.6069602
                            ],
                            [
                                121.0045971,
                                14.6072271
                            ],
                            [
                                121.0048208,
                                14.6075007
                            ],
                            [
                                121.005031,
                                14.6077633
                            ],
                            [
                                121.0061786,
                                14.6068949
                            ],
                            [
                                121.0064076,
                                14.6071782
                            ],
                            [
                                121.0066206,
                                14.6074388
                            ],
                            [
                                121.006848,
                                14.6077207
                            ],
                            [
                                121.0070634,
                                14.6079867
                            ],
                            [
                                121.0072815,
                                14.6082547
                            ],
                            [
                                121.0075131,
                                14.60854
                            ],
                            [
                                121.0077267,
                                14.6088031
                            ],
                            [
                                121.0079478,
                                14.6090754
                            ],
                            [
                                121.0081713,
                                14.6093507
                            ],
                            [
                                121.0083959,
                                14.6096274
                            ],
                            [
                                121.0086186,
                                14.6099017
                            ],
                            [
                                121.0088347,
                                14.6101679
                            ],
                            [
                                121.0099892,
                                14.6092935
                            ],
                            [
                                121.0102079,
                                14.6095589
                            ],
                            [
                                121.0104299,
                                14.6098411
                            ]
                        ]
                    },
                    "properties": {}
                }
            ]
        },
        "message": "Safe route found."
    }

def test_checkCoordinates():
    url = f"{API_BASE_URL}/checkCoordinates"
    response = requests.post(
        url,
        json={
            "coordinates": [
                121.05959688150006, 
                14.590127718074672
            ]
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "true"
    }

def test_add_request():
    url = f"{API_BASE_URL}/add_request"
    response = requests.post(
        url,
        json={
            "person_id": 3,
            "coordinates": [
                {"coordinates": ["121.0694063","14.65679956"]},
                {"coordinates": ["121.0411614","14.66310851"]},
                {"coordinates": ["121.0219046","14.65919254"]},
                {"coordinates": ["121.0177288","14.65537632"]}
            ]
        }
    )

    assert response.status_code == 200
    assert "request_id" in response.json()

def test_get_route_info():
    url = f"{API_BASE_URL}/get_route_info"
    response = requests.post(
        url,
        json={
        "route_id": 1
        }
    )

    assert response.status_code == 200
    assert "payload" in response.json()

def test_save_route():
    url = f"{API_BASE_URL}/save_route"
    response = requests.post(
        url,
        json={
        "request_id": 1,
        "points": {
            "start": {
            "coordinates": [
                121.04932,
                14.65491
            ]
            },
            "other_points": [
            {
                "coordinates": [
                121.07471,
                14.66651
                ]
            }
            ]
        }
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True
    }


def test_update_rescued():
    url = f"{API_BASE_URL}/update_rescued"
    response = requests.post(
        url,
        json={
        "request_id": 0
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "done"
    }

