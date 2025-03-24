from typing import Tuple
from typing import List
from geopy import distance

# Placeholder for flooded areas and R-tree index
FLOODED_AREAS = None
FLOOD_INDEX = None

# Placeholder for road network cache
ROAD_NETWORK_CACHE = {}

# Define flood exposure thresholds
HIGH_EXPOSURE_THRESHOLD = 900  # 300 meters of flood exposure to risk 3
MEDIUM_EXPOSURE_THRESHOLD = 450  # 150 meters of flood exposure to risk 3

FLOOD_WEIGHTS = {
    "1": 1,
    "2": 2,
    "3": 3,
}


def get_flood_index():
    global FLOOD_INDEX
    return FLOOD_INDEX


def set_flood_index(index):
    global FLOOD_INDEX
    FLOOD_INDEX = index


def get_flooded_areas():
    global FLOODED_AREAS
    return FLOODED_AREAS


def set_flooded_areas(areas):
    global FLOODED_AREAS
    FLOODED_AREAS = areas


def get_road_network_cache():
    global ROAD_NETWORK_CACHE
    return ROAD_NETWORK_CACHE


def set_road_network_cache(cache, key):
    global ROAD_NETWORK_CACHE
    ROAD_NETWORK_CACHE[key] = cache


def calculate_geodesic_distance(
    point1: Tuple[float, float], point2: Tuple[float, float]
) -> float:
    # Calculate the geodesic distance between two points in kilometers
    return distance.distance(point1, point2).km


def calculate_distance(route: List[Tuple[float, float]]) -> float:
    return sum(
        calculate_geodesic_distance(route[i], route[i + 1])
        for i in range(len(route) - 1)
    )


def calculate_duration(distance_meters: int, average_speed: float = 5.0) -> float:
    """Calculate the estimated duration in minutes based on distance and average walking speed."""
    return (distance_meters / 1000) / average_speed * 60
