from fastapi import HTTPException, status
import time

from routing.geojson import create_geojson
from models import Route, DirectionsResponse, DirectionsRequest
from routing.main_routing import compute_best_route_from_request
from routing.cache_database import (
    write_to_database,
)

async def directions(directionRequest: DirectionsRequest) -> DirectionsResponse:
    start_time = time.time()
    try:
        (
            hashed_id,
            duration_minutes,
            total_distance_km,
            route_coordinates,
            # route_info,
            route_data,
        ) = await compute_best_route_from_request(
            directionRequest.start, directionRequest.end
        )

        if route_data:
            route_data = DirectionsResponse.model_validate(route_data)

            end_time = time.time()
            print(f"Full running time: {end_time - start_time:.2f} seconds")

            return route_data

        geojson = create_geojson(route_coordinates)

        if duration_minutes:
            # Write the route to the cache database

            route_data = DirectionsResponse(
                route=Route(
                    duration=duration_minutes,
                    distanceKm=total_distance_km,
                    # coordinates=route_coordinates,
                    # routeInfo=route_info,
                ),
                geojson=geojson,
                message="Safe route found.",
            )

            await write_to_database(
                hashed_id,
                route_data.model_dump_json(),
            )

            end_time = time.time()
            print(f"Full running time: {end_time - start_time:.2f} seconds")

            return route_data
        else:
            # Return an error message if no safe route is found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No safe route found.",
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
