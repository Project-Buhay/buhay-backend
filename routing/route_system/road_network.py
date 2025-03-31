from typing import Tuple, List
import networkx as nx
import osmnx as ox
import concurrent.futures
import asyncio
from networkx.readwrite import json_graph
from shapely.geometry import LineString, Point, Polygon
import json

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
from routing.cache_database import save_qc_road_network_to_db, get_qc_road_network_cache


class ShapelyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, LineString):
            return {"type": "LineString", "coordinates": list(obj.coords)}
        elif isinstance(obj, Point):
            return {"type": "Point", "coordinates": list(obj.coords)[0]}
        elif isinstance(obj, Polygon):
            return {"type": "Polygon", "coordinates": [list(obj.exterior.coords)]}
        return super().default(obj)


async def get_road_network() -> nx.Graph:

    # Get the road network cache
    road_network_cache = get_road_network_cache()

    # Check if the road network is already in the cache
    if "QUEZON_CITY" in road_network_cache:
        return road_network_cache["QUEZON_CITY"]


async def get_quezon_city_road_network() -> nx.Graph:
    # Load the road network from the database
    G = await load_road_network_from_db()

    # Check if the road network is already in the cache
    if G:
        set_road_network_cache(G, "QUEZON_CITY")
        return G

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

    # Save to postgresql
    await save_road_network_to_db(G)

    set_road_network_cache(G, "QUEZON_CITY")

    return G


async def save_road_network_to_db(G: nx.Graph):
    graph_data = json_graph.node_link_data(G)
    json_data = json.dumps(graph_data, cls=ShapelyEncoder)

    await save_qc_road_network_to_db(json_data)


async def load_road_network_from_db() -> nx.Graph:
    # Load the road network from the database
    result = await get_qc_road_network_cache()

    if not result:
        return None

    # The fetch() method returns a list of records, so we need to extract the data field
    if isinstance(result, list) and len(result) > 0:
        # Extract the first row's 'data' column
        data = result[0]["data"]

        # Load the graph from the json data
        graph_data = json.loads(data)
        G = json_graph.node_link_graph(graph_data)
        return G

    return None
