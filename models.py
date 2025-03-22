from pydantic import BaseModel
from typing import List, Tuple


class RouteInfo(BaseModel):
    instruction: str
    distance: float  # Distance in kilometers


class Route(BaseModel):
    duration: float
    distanceKm: float
    # coordinates: List[List[float]]
    # routeInfo: List[RouteInfo]


class DirectionsResponse(BaseModel):
    route: Route
    geojson: dict
    message: str = None


class DirectionsRequest(BaseModel):
    # Format: "lng,lat"
    # Example: "121.07471,14.66651"
    start: str
    end: str


class Point(BaseModel):
    # (lng, lat)
    coordinates: Tuple[float, float]


class TSPinput(BaseModel):
    start: Point
    other_points: List[Point]


class TSPOutput(BaseModel):
    start: str
    end: str
    data: DirectionsResponse


class LoginInput(BaseModel):
    username: str
    password: str


class AddRequestInput(BaseModel):
    person_id: int
    coordinates: List[Point]


class SaveRouteInput(BaseModel):
    request_id: int
    points: TSPinput


class RouteInfo(BaseModel):
    route_id: int


class UpdateRescued(BaseModel):
    request_id: int
