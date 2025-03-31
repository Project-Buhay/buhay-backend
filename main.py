from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from typing import AsyncGenerator
import json
from typing import List
import osmnx as ox

from routing.load_data import load_flooded_areas
from tsp_endpoint import main_tsp
from tests.naive_tsp import naive_tsp  # For testing

from database_endpoints import (
    convert_coordinates,
    login,
    add_request,
    get_route_info,
    save_route,
    update_rescued,
    update_ongoing_endpoint,
    get_rescuers,
    assign,
)

from routing.route_directions import directions
from models import DirectionsRequest
from routing.cache_database import (
    connect_to_database,
    close_database_connection,
)
from models import Point, AddRequestInput
from qc_coordinates import check_point_in_polygon
from own_websocket import own_socket
from routing.route_system.road_network import (
    get_quezon_city_road_network,
    get_road_network,
)


# Load the flooded areas on startup
@asynccontextmanager
async def startup_event(app: FastAPI) -> AsyncGenerator[None, None]:
    await load_flooded_areas()
    await connect_to_database()
    await get_quezon_city_road_network()
    await own_socket.start_db_listener()
    yield
    await close_database_connection()


# Initialize the FastAPI app
app = FastAPI(lifespan=startup_event)

# Include router for tsp endpoint
app.include_router(main_tsp.router)
app.include_router(naive_tsp.router)  # For testing
app.include_router(own_socket.router)
app.include_router(login.router)
app.include_router(convert_coordinates.router)
app.include_router(add_request.router)
app.include_router(get_route_info.router)
app.include_router(save_route.router)
app.include_router(update_rescued.router)
app.include_router(update_ongoing_endpoint.router)
app.include_router(get_rescuers.router)
app.include_router(assign.router)


# app.include_router(route_directions.router)
@app.post("/directions", status_code=status.HTTP_200_OK)
async def call_directions(directionRequest: DirectionsRequest):
    return await directions(directionRequest)


@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    return {"message": "pong"}


@app.post("/checkCoordinates", status_code=status.HTTP_200_OK)
async def checkCoordinates(point: Point):
    if await check_point_in_polygon(point.coordinates):
        return {"message": "true"}
    return {"message": "false"}


@app.get("/test", status_code=status.HTTP_200_OK)
async def test():
    with open("sample_data.json", "r") as f:
        json_data = json.load(f)
    return json_data


@app.post("/compare_coordinates", status_code=status.HTTP_200_OK)
async def compare_coordinates(point: AddRequestInput):
    lst = []
    road_network_cache = await get_road_network()
    for p in point.coordinates:
        lst.append(
            get_nearest_nodes(road_network_cache, p.coordinates[0], p.coordinates[1])
        )
    if len(lst) == len(set(lst)):
        return {"message": "true"}
    return {"message": "false"}


def get_nearest_nodes(G, lng, lat):
    node = ox.nearest_nodes(G, lng, lat)
    return node
