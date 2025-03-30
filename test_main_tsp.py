import pytest
# import warnings
# import json

# from typing import List

# from fastapi import status
from httpx import ASGITransport, AsyncClient
from main import app, startup_event
# from models import Point, TSPinput

# from random import randint
# from time import time
# from pprint import pprint


# from tests.naive_tsp import naive_tsp # For testing
# from models import TSPinput
# from tests.naive_tsp.structs import Graph, Path, Coordinates
# from tests.naive_tsp.utils import naive_create_graph, min_hamiltonian_paths, path_to_json_parser

# from osmnx.distance import great_circle

# def total_haversine(points, n):
#     total = 0
#     for i in range(n):
#         total += great_circle(points[i]["coordinates"][1], points[i]["coordinates"][0],points[i+1]["coordinates"][1], points[i+1]["coordinates"][0])
#     return total

# def generate_points(n: int) -> TSPinput:
#     start: Point = {"coordinates": [randint(0, 100_000), randint(0, 100_000)]}
#     other_points: List[Point] = list()
#     for i in range(n-1):
#         lat = float(randint(0, 100_000))
#         lng = float(randint(0, 100_000))
#         p = {"coordinates":[lng,lat]}
#         other_points.append(p)
#     ret: TSPinput = {
#         "start": start,
#         "other_points": other_points
#     }
#     return ret
  
# @pytest.mark.asyncio
# async def test_tsp():
#     start = time()
#     async with startup_event(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
#             request = client.build_request(url="/tsp", method="GET", 
#                 json={
#                     "start": {"coordinates": [1,1]},
#                     "other_points": [
#                         {"coordinates": [10, 10]},
#                         {"coordinates": [2, 2]},
#                         {"coordinates": [0, 0]}
#                     ]
#                 }
#             )
#             response = await client.send(request)

#         end = time()
#         # print("TIME TAKEN: ", end-start)
#         print(response.json(), total_haversine(response.json(), 4))
#         print(total_haversine([
#             {"coordinates": [1.0, 1.0]},
#             {"coordinates": [0.0, 0.0]},
#             {"coordinates": [2.0, 2.0]},
#             {"coordinates": [10.0,10.0]},
#             {"coordinates": [1.0, 1.0]},
#         ], 4))
#         assert response.json() == [
#             {"coordinates": [1.0, 1.0]},
#             {"coordinates": [0.0, 0.0]},
#             {"coordinates": [10.0, 10.0]},
#             {"coordinates": [2.0, 2.0]},
#             {"coordinates": [1.0, 1.0]},
#         ]

# @pytest.mark.asyncio
# async def test_time():
#     test_cases = 6
#     n = 6
#     total_start = time()
#     for i in range(test_cases):
#         body = generate_points(n)
#         pprint(body)
#         start = time()
#         async with startup_event(app):
#             async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
#                 request = client.build_request(url="/tsp", method="GET", json=body)
#                 response = await client.send(request)

#     total_end = time()
#     print()
#     print(f"TIME TAKEN FOR n={n} {test_cases} TEST CASES: ", total_end-total_start)
#     print(f"AVERAGE TIME FOR n={n} {test_cases} TEST CASES: ", (total_end-total_start)/test_cases)

# async def tsp_case(inp: TSPinput):
#     async with startup_event(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as tsp_client:
#             request = tsp_client.build_request(url="/tsp", method="GET", json=inp)
#             tsp_response = await tsp_client.send(request)

#         tsp_json = tsp_response.json()
#         print(f'/tsp: {tsp_json}, distance: {total_haversine(tsp_json, len(inp["other_points"])+1)}')
#         print()
    
#     return tsp_json


# async def naive_tsp_case(inp: TSPinput):
#     async with startup_event(app):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as naive_tsp_client:
#             request = naive_tsp_client.build_request(url="/naive_tsp", method="GET", json=inp)
#             naive_tsp_response = await naive_tsp_client.send(request)

#         naive_tsp_json = naive_tsp_response.json()
#         print(f'/naive_tsp: {naive_tsp_json}, distance: {total_haversine(naive_tsp_json, len(inp["other_points"])+1)}')
#         print()

#     return naive_tsp_json


# @pytest.mark.asyncio
# async def test_correctness():
#     test_cases = 10 # The brute force solver might be very, very slow

#     print(f'Testing Correctness...')
#     total_start = time()

#     for i in range(test_cases):
#         n = 6
#         inp = generate_points(n)
#         print(f'{i}: {inp}')
#         print()

#         tsp_result = await tsp_case(inp)
#         naive_tsp_result = await naive_tsp_case(inp)
#         assert(tsp_result == naive_tsp_result)

#     total_end = time()

#     print(f'Total time: {total_end - total_start}')
#     print(f'Average time per test case: {(total_end - total_start) / test_cases}')

@pytest.mark.asyncio
async def test_tsp():
    async with startup_event(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            request = client.build_request(url="/tsp", method="POST", 
                json= {
                    "start": {"coordinates": [121.0696276, 14.6567504]},
                    "other_points": [
                        {"coordinates": [121.0698762, 14.6536758]}
                    ]
                }
            )
            response = await client.send(request)

        assert response.json() == [
            {
                "start": [121.0696276, 14.6567504],
                "end": [121.0698762, 14.6536758],
                "data": {
                    "route": {
                        "duration": 8.76583198384868,
                        "distanceKm": 0.7304859986540565
                    },
                    "geojson": {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "geometry": {
                                    "type": "LineString",
                                    "coordinates": [
                                        [121.0698801, 14.6537622],
                                        [121.0698984, 14.6537919],
                                        [121.0698968, 14.653819],
                                        [121.0699702, 14.653818],
                                        [121.0699698, 14.6539568],
                                        [121.0704004, 14.6539652],
                                        [121.070528, 14.6539677],
                                        [121.0707416, 14.654112],
                                        [121.0707382, 14.6544471],
                                        [121.0707296, 14.6551461],
                                        [121.0707226, 14.6555607],
                                        [121.0707388, 14.6560546],
                                        [121.0707449, 14.6561442],
                                        [121.0706345, 14.6561433],
                                        [121.0706336, 14.6563262],
                                        [121.0706319, 14.6566677],
                                        [121.0703873, 14.6566702],
                                        [121.0698002, 14.6575488],
                                        [121.0692788, 14.6575483],
                                        [121.0692923, 14.6571388],
                                        [121.0692924, 14.6570228],
                                        [121.0692926, 14.6566825],
                                        [121.069507, 14.6566822]
                                    ]
                                },
                                "properties": {}
                            }
                        ]
                    },
                    "message": "Safe route found."
                }
            },
            {
                "start": [121.0698762, 14.6536758],
                "end": [121.0696276, 14.6567504],
                "data": {
                    "route": {
                        "duration": 8.76583198384868,
                        "distanceKm": 0.7304859986540565
                    },
                    "geojson": {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "geometry": {
                                    "type": "LineString",
                                    "coordinates": [
                                        [121.069507, 14.6566822],
                                        [121.0692926, 14.6566825],
                                        [121.0692924, 14.6570228],
                                        [121.0692923, 14.6571388],
                                        [121.0692788, 14.6575483],
                                        [121.0698002, 14.6575488],
                                        [121.0703873, 14.6566702],
                                        [121.0706319, 14.6566677],
                                        [121.0706336, 14.6563262],
                                        [121.0706345, 14.6561433],
                                        [121.0707449, 14.6561442],
                                        [121.0707388, 14.6560546],
                                        [121.0707226, 14.6555607],
                                        [121.0707296, 14.6551461],
                                        [121.0707382, 14.6544471],
                                        [121.0707416, 14.654112],
                                        [121.070528, 14.6539677],
                                        [121.0704004, 14.6539652],
                                        [121.0699698, 14.6539568],
                                        [121.0699702, 14.653818],
                                        [121.0698968, 14.653819],
                                        [121.0698984, 14.6537919],
                                        [121.0698801,14.6537622]
                                    ]
                                },
                                "properties": {}
                            }
                        ]
                    },
                    "message": "Safe route found."
                }
            }
        ]