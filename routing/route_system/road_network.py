from typing import Tuple, List
import networkx as nx
import osmnx as ox
import concurrent.futures
import asyncio

from routing.global_variables import (
    get_road_network_cache,
    set_road_network_cache,
    calculate_geodesic_distance,
)
from routing.route_system.flood_risk_computations import (
    compute_flood_risk,
    assign_edge_flood_risk,
)


async def get_road_network(
    start: Tuple[float, float], end: Tuple[float, float]
) -> nx.Graph:

    # Get the road network cache
    road_network_cache = get_road_network_cache()

    # Initialize the key for the cache to be the start and end coordinates
    key = (start, end)

    # Check if the road network is already in the cache
    if key in road_network_cache:
        return road_network_cache[key]

    # Calculate the bounding box for the road network
    distance = calculate_geodesic_distance(start, end)
    # Reducing the buffer size below 0.01 improves the time taken to compute the flood risk
    # However, it may result in a less accurate route or route is cut off due to the buffer size
    buffer = min(0.01, distance * 0.01)

    north = max(start[0], end[0]) + buffer
    south = min(start[0], end[0]) - buffer
    east = max(start[1], end[1]) + buffer
    west = min(start[1], end[1]) - buffer

    # Get the road network graph
    bbox = (west, south, east, north)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        G = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: ox.graph_from_bbox(bbox, network_type="walk", simplify=True),
        )

    # Compute the flood risk for each node
    await compute_flood_risk(G, list(G.nodes))

    # Assign flood risk to edges based on node flood risks
    await assign_edge_flood_risk(G)

    # Add the road network to the cache
    set_road_network_cache(G, key)

    return G
