from fastapi import APIRouter, HTTPException, status
from fastapi.params import Body

from models import Point, TSPinput, DirectionsRequest, DirectionsResponse
from routing.route_directions import directions
from tsp_endpoint.auxiliary_functions import create_graph, append_starting_node, node_to_json_parser
import networkx as nx
from typing import List


router = APIRouter()

@router.post("/tsp", status_code = status.HTTP_200_OK)
async def tsp(points: TSPinput):
    try:
        # Convert input points into a complete, weighted, directed graph, in which the weights of the edges are the haversine distance between the adjacent vertices.
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
        
        # Connect the starting node to the closest end of the shortest hamiltonian path.
        # tsp_route = append_starting_node(tsp_route, points.start)

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
    
    except nx.NetworkXError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "If G is a directed graph it has to be strongly connected or the complete version cannot be generated."
        )

    except ValueError as e:
        # Handle specific exceptions with a 400 Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.",
        )

    except HTTPException as e:
        # Re-raise HTTPExceptions
        raise e

    except Exception as e:
        # Handle unexpected server errors with a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )