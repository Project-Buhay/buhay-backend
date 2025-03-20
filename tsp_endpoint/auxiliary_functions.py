import networkx as nx
from osmnx.distance import great_circle
from models import Point
from typing import List

def create_graph(points: List[Point]) -> nx.Graph: 
    n = len(points) 
    G = nx.Graph()

    # Add points[i] as the ith node of the graph
    for i in range(n):
        G.add_node(
            i, 
            lng = points[i].coordinates[0], 
            lat = points[i].coordinates[1]
        )
    
    # Add edge(i,j) for each possible i,j combination such that its weight is the haversine distance between Point i and Point j
    for i in range(n):
        lng_i, lat_i = points[i].coordinates
        for j in range(i+1, n):
            lng_j, lat_j = points[j].coordinates
            haversine_distance = great_circle(lat_i, lng_i, lat_j, lng_j)
            G.add_edge(
                i, j,
                weight = haversine_distance
            )
    
    return G

def append_starting_node(tsp_route: List[Point], start: Point) -> List[Point]:
    # Compare the haversine distance between the starting node and each end of the hamiltonian path containing nodes 1 to n-1.
    # Put starting node 0 next to the hamiltonian end node that is closer.
    # Reverse the output list if the starting node was put on the right end of the list.

    lng_0, lat_0 = start.coordinates[0], start.coordinates[1]
    left_end = tsp_route[0]
    lng_left, lat_left = left_end['coordinates'][0], left_end['coordinates'][1]
    right_end = tsp_route[-1]
    lng_right, lat_right = right_end['coordinates'][0], right_end['coordinates'][1]

    if great_circle(lat_0, lng_0, lat_left, lng_left) < great_circle(lat_0, lng_0, lat_right, lng_right): 
        complete_tsp: List[Point] = [start] + tsp_route
    else:
        complete_tsp: List[Point] = [start] + tsp_route[::-1]

    return complete_tsp

def node_to_json_parser(G: nx.Graph, nodes: List[int]) -> List[dict[str, List[float]]]:
    ret: List[dict[str, List[float]]] = []
    for node in nodes:
        ret.append({
            "coordinates": [G.nodes[node]["lng"], G.nodes[node]["lat"]]
        })
    return ret