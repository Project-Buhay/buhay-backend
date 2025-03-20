from fastapi import APIRouter, HTTPException, status
from typing import List

from models import TSPinput
from tests.naive_tsp.structs import Graph, Path, Coordinates
from tests.naive_tsp.utils import naive_create_graph, min_hamiltonian_paths, path_to_json_parser



router = APIRouter()

@router.get("/naive_tsp", status_code = status.HTTP_200_OK)
async def naive_tsp(points: TSPinput) -> List[dict[str, Coordinates]]:
    """
    This should return a minimal Hamiltonian path
    that starts at a given starting node (points.start).

    The tsp implementation for this test file must be naive.
    """
    try:
        # Convert input points into a complete, weighted, directed graph, 
        # in which the weights of the edges are the haversine distance between the adjacent vertices.
        G: Graph = naive_create_graph([points.start] + points.other_points)

        # Testing NetworkX `traveling_salesman_problem()`.

        # Search for the shortest acyclic hamiltonian path connecting all points.
        # Get the first one na lang, though there can be more.
        tsp_route: Path = min_hamiltonian_paths(G)[0]

        # Return a JSONable dict of a list of points.
        return path_to_json_parser(tsp_route)
    
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