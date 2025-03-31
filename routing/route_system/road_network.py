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
from qc_coordinates import QUEZON_CITY


async def get_road_network() -> nx.Graph:

    # Get the road network cache
    road_network_cache = get_road_network_cache()

    # Check if the road network is already in the cache
    if "QUEZON_CITY" in road_network_cache:
        return road_network_cache["QUEZON_CITY"]


async def get_quezon_city_road_network() -> nx.Graph:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        G = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: ox.graph_from_polygon(
                QUEZON_CITY, network_type="all", simplify=True
            ),
        )

    # Compute the flood risk for each node
    await compute_flood_risk(G, list(G.nodes))

    # Assign flood risk to edges based on node flood risks
    await assign_edge_flood_risk(G)

    set_road_network_cache(G, "QUEZON_CITY")

    return G
