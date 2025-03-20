from osmnx.distance import great_circle
from typing import List

from models import Point
from tests.naive_tsp.structs import Node, Graph, Path, Coordinates



def naive_create_graph(points: List[Point]) -> Graph: 
    """
    Convert to a complete, weighted, directed graph, in which the weights of the edges
    are the haversine distance between the adjacent vertices.
    """
    n = len(points) 
    G = Graph()

    # Add points[i] as the ith node of the graph
    for i in range(n):
        G.add_node(
            i,
            lat = points[i].coordinates[1], 
            lng = points[i].coordinates[0]
        )
    
    # Add edge (i, j) for each possible i, j combination such that its weight 
    # is the haversine distance between Point i and Point j
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


def h_paths(G: Graph, s: Node, start: Node, visited: dict[int, bool], distance_to_start: float = 0) -> List[Path]:
    """
    Get all single-source hamiltonian paths _naively_ using dynamic programming.
    Hopefully this is reasonably slow lang.
    """
    visited[start.i] = True

    if all(visited.values()):
        visited[start.i] = False
        return [(distance_to_start + great_circle(start.lat, start.lng, s.lat, s.lng), [start, s])]

    paths: List[Path] = []

    # Get adjacent edges.
    connected_edges = list(filter((
            lambda edge : edge.i == start.i 
            and not visited[G.get_node(edge.j).i]
        ), G.edges
    ))

    # Add starting node to paths from its adjacent nodes.
    for edge in connected_edges:
        adj = h_paths(G, s, G.get_node(edge.j), visited, distance_to_start + edge.weight)
        for distance_to_adj, adj_path in adj:
            paths += [(distance_to_adj, [start] + adj_path)]

    visited[start.i] = False

    return paths


def min_hamiltonian_paths(G: Graph) -> List[Path]:
    # Get all minimum hamiltonian paths given a starting node.
    start_node = G.nodes[0] # Added the starting point kanina as the first node in the graph.
    all_paths: List[Path] = h_paths(G, start_node, start_node, {n.i: False for n in G.nodes})

    # Get the shortest distance among all paths.
    shortest_distance = min(all_paths, key=lambda p : p[0])[0]

    # Get all paths with the shortest distance; at best, there's just one path.
    shortest_paths = list(filter(lambda p : p[0] == shortest_distance, all_paths))

    # Return a list of paths.
    return shortest_paths


def path_to_json_parser(path: Path) -> List[dict[str, Coordinates]]:
    # Get the order of nodes in the path.
    _, node_path = path

    # Get all points in node_path and make them JSONable.
    # Type should be dict[str, Any] pero since one attribute lang naman, make it strict na.
    point_path: List[dict[str, Coordinates]] = [
        Point(coordinates=(node.lng, node.lat)).model_dump(mode='json')
        for node in node_path
    ]

    # Return a JSONable dict of a list of points.
    return point_path