from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from typing import AsyncGenerator
import json

from routing.load_data import load_flooded_areas
from tsp_endpoint import main_tsp
from tests.naive_tsp import naive_tsp  # For testing

from database_endpoints import (
    convert_coordinates,
    login_endpoint,
    add_request,
    get_route_info,
    save_route,
    update_rescued,
    update_ongoing_endpoint,
)

from routing.route_directions import directions
from models import DirectionsRequest
from routing.cache_database import (
    connect_to_database,
    close_database_connection,
)
from models import Point
from qc_coordinates import check_point_in_polygon
from own_websocket import own_socket


# Load the flooded areas on startup
@asynccontextmanager
async def startup_event(app: FastAPI) -> AsyncGenerator[None, None]:
    await load_flooded_areas()
    await connect_to_database()
    await own_socket.start_db_listener()
    yield
    await close_database_connection()


# Initialize the FastAPI app
app = FastAPI(lifespan=startup_event)

# Include router for tsp endpoint
app.include_router(main_tsp.router)
app.include_router(naive_tsp.router)  # For testing
app.include_router(own_socket.router)
app.include_router(login_endpoint.router)
app.include_router(convert_coordinates.router)
app.include_router(add_request.router)
app.include_router(get_route_info.router)
app.include_router(save_route.router)
app.include_router(update_rescued.router)
app.include_router(update_ongoing_endpoint.router)


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
