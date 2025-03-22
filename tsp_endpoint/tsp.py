from models import TSPinput, DirectionsRequest
from routing.route_directions import directions
from tsp_endpoint.auxiliary_functions import create_graph, node_to_json_parser
import networkx as nx
import json

async def tsp(points: TSPinput):
    G: nx.Graph = create_graph([points.start] + points.other_points)

    # Search for the shortest acyclic hamiltonian path connecting all other_points.
    tsp_route = nx.approximation.traveling_salesman_problem(
        G = G,
        nodes = list(G.nodes),
        weight = "weight",
        cycle = True,
        method = nx.approximation.simulated_annealing_tsp,
        init_cycle = nx.approximation.greedy_tsp(G, "weight")
    )
    while tsp_route[0] != 0:
        front = tsp_route.pop(0)
        tsp_route.append(front)
    tsp_route = node_to_json_parser(G, tsp_route)

    dir = []
    for pt in range(1, len(tsp_route)):
        req = DirectionsRequest(
            start=f'{tsp_route[pt]["coordinates"][0]}, {tsp_route[pt]["coordinates"][1]}', 
            end=f'{tsp_route[pt - 1]["coordinates"][0]}, {tsp_route[pt - 1]["coordinates"][1]}'
        )
        
        to_append = {
            'start': tsp_route[pt - 1]['coordinates'],
            'end': tsp_route[pt]['coordinates'],
            'data': await directions(req)
        }

        dir.append(to_append)

    return dir