from typing import Tuple
import networkx as nx
import osmnx as ox


def get_maneuver(G: nx.Graph, u: int, v: int, w: int) -> str:
    """Determine the maneuver based on the angle between three nodes."""
    if u == v:  # Starting point
        return "Head"
    if v == w:  # Ending point
        return "Arrive"

    angle = ox.bearing.calculate_bearing(
        G.nodes[u]["y"], G.nodes[u]["x"], G.nodes[v]["y"], G.nodes[v]["x"]
    ) - ox.bearing.calculate_bearing(
        G.nodes[v]["y"], G.nodes[v]["x"], G.nodes[w]["y"], G.nodes[w]["x"]
    )

    angle = (angle + 360) % 360

    if angle < 10:
        return "Continue straight"
    elif 10 <= angle < 45:
        return "Slight right"
    elif 45 <= angle < 135:
        return "Right"
    elif 135 <= angle < 225:
        return "U-turn"
    elif 225 <= angle < 315:
        return "Left"
    else:
        return "Slight left"


def format_distance(distance: float) -> str:
    if distance < 100:
        return f"{int(distance)} meters"
    elif distance < 1000:
        return f"{int(distance / 10) * 10} meters"
    else:
        return f"{distance / 1000:.1f} km"


def get_cardinal_direction(start: Tuple[float, float], end: Tuple[float, float]) -> str:
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

    if turn_angle < 10 or turn_angle > 350:
        return "Continue straight"
    elif 10 <= turn_angle < 170:
        return "Turn right"
    elif 190 <= turn_angle < 350:
        return "Turn left"
    else:
        return "Make a U-turn"
