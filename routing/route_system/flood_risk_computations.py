import asyncio
from typing import Tuple, List
import networkx as nx
from shapely.geometry import Point
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import osmnx as ox

from routing.global_variables import (
    get_flood_index,
    get_flooded_areas,
    FLOOD_WEIGHTS,
)

MAX_EFFECT_DISTANCE = 0.01  # About 1km in degrees


async def compute_flood_risk(graph: nx.Graph, nodes: List[int]) -> None:
    # Compute the flood risk for each node

    # Get the event loop and chunk size
    loop = asyncio.get_event_loop()
    chunk_size = 1000

    # Iterate over the nodes in chunks
    for i in range(0, len(nodes), chunk_size):
        chunk = nodes[i : i + chunk_size]
        flood_risks = await loop.run_in_executor(
            ThreadPoolExecutor(),
            lambda: {
                # compute the flood risk for each node
                u: calculate_flood_risk((graph.nodes[u]["y"], graph.nodes[u]["x"]))
                for u in chunk
            },
        )

        # Assign the flood risk to the nodes
        for u, risk in flood_risks.items():
            graph.nodes[u]["flood_risk"] = risk


@lru_cache(maxsize=10000)
def calculate_flood_risk(point: Tuple[float, float]) -> float:
    # Calculate the flood risk at a given point

    # Get the flood index and flooded areas data
    flood_index = get_flood_index()
    flooded_areas = get_flooded_areas()

    flood_weights = FLOOD_WEIGHTS

    # Initialize variables for nearby areas, distances, closest distances, and risk
    nearby_areas = {}
    distances = {}
    closest_distance = {}
    risk = 0

    # Create a point geometry from the input coordinates
    point_geom = Point(point)

    # Find the nearby areas for each flood data file
    for key, idx in flood_index.items():
        nearby_areas[key] = list(idx.intersection(point_geom.bounds))

    # If there are no nearby areas, return 0.0
    if all(not areas for areas in nearby_areas.values()):
        return 0.0

    # Calculate the distances to the flooded areas
    for key, areas in nearby_areas.items():
        distances[key] = [point_geom.distance(flooded_areas[key][i]) for i in areas]

    # Find the closest distance to each flooded area
    for key, dists in distances.items():
        if dists:
            closest_distance[key] = min(dists)

    # Calculate the flood risk based on the closest distances and flood weights
    for key, distance in closest_distance.items():
        level_risk = flood_weights.get(key, 0) - (distance / MAX_EFFECT_DISTANCE)
        risk = max(risk, level_risk)

    return risk


async def assign_edge_flood_risk(G: nx.Graph) -> None:
    # Assign flood risk to edges based on node flood risks

    for u, v, d in G.edges(data=True):
        # Calculate the average flood risk for the edge
        u_risk = G.nodes[u].get("flood_risk", 0)
        v_risk = G.nodes[v].get("flood_risk", 0)
        d["flood_risk"] = (u_risk + v_risk) / 2
