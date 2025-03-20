from typing import Tuple
import networkx as nx
from typing import List
from geopy import distance
import osmnx as ox


def get_street_name(G: nx.Graph, u: int, v: int) -> str:
    # Get the street name for the edge between two nodes
    edge_data = G.get_edge_data(u, v, 0)
    if "name" in edge_data:
        return edge_data["name"]
    return "Unnamed Street"


def get_cardinal_direction(start: Tuple[float, float], end: Tuple[float, float]) -> str:
    # Calculate the cardinal direction from the start to the end point
    angle = ox.bearing.calculate_bearing(start[0], start[1], end[0], end[1])
    directions = [
        "north",
        "northeast",
        "east",
        "southeast",
        "south",
        "southwest",
        "west",
        "northwest",
    ]
    index = round(angle / 45) % 8
    return directions[index]


def get_turn_direction(
    start: Tuple[float, float],
    a: Tuple[float, float],
    b: Tuple[float, float],
    c: Tuple[float, float],
) -> str:
    # Calculate the initial bearing from the start point
    initial_bearing = ox.bearing.calculate_bearing(start[0], start[1], a[0], a[1])

    # Calculate the bearings for the two segments
    bearing1 = ox.bearing.calculate_bearing(a[0], a[1], b[0], b[1])
    bearing2 = ox.bearing.calculate_bearing(b[0], b[1], c[0], c[1])

    # Normalize the bearings relative to the initial bearing
    angle1 = (bearing1 - initial_bearing + 360) % 360
    angle2 = (bearing2 - initial_bearing + 360) % 360

    # Calculate the turn angle
    turn_angle = (angle2 - angle1 + 360) % 360

    # Determine the turn direction based on the angle
    if turn_angle < 10 or turn_angle > 350:
        return "Continue straight"
    elif 10 <= turn_angle < 170:
        return "Turn right"
    elif 190 <= turn_angle < 350:
        return "Turn left"
    else:
        return "Make a U-turn"
