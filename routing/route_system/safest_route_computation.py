from typing import List, Tuple
import networkx as nx
import osmnx as ox

from models import RouteInfo
from routing.global_variables import calculate_geodesic_distance
from routing.route_system.road_network import get_road_network
from routing.route_system.weight import weight_function


# Function to find the safest route between two points
async def find_safest_route(
    start: Tuple[float, float], end: Tuple[float, float]
) -> Tuple[List[Tuple[float, float]], List[List[float]], List[RouteInfo]]:

    # Get the road network graph
    G = await get_road_network(start, end)

    # Find the nearest nodes to the start and end coordinates
    start_node = ox.nearest_nodes(G, start[1], start[0])
    end_node = ox.nearest_nodes(G, end[1], end[0])

    #  Find the safest route using A* algorithm
    try:
        path = nx.astar_path(
            G,
            start_node,
            end_node,
            heuristic=lambda u, v: calculate_geodesic_distance(
                (G.nodes[u]["y"], G.nodes[u]["x"]), (G.nodes[v]["y"], G.nodes[v]["x"])
            ),
            weight=weight_function,
        )

        # Get the route coordinates
        route = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in path]

        # Get the route information
        coordinates = [[coord[1], coord[0]] for coord in route]  # [lng, lat]

        return route, coordinates, G, path, route

    except nx.NetworkXNoPath:
        return None, None, None, None, None
