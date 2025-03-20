from fastapi import APIRouter, HTTPException, status
from models import Point
import json
from typing import List
import googlemaps
router = APIRouter()

from db_env import GOOGLE_MAPS_API
gmaps = googlemaps.Client(key = GOOGLE_MAPS_API)

@router.get("/convert_coordinates", status_code = status.HTTP_200_OK)
async def convert_coordinates(points: list[Point]):
    try:
        location_names: list[str]= list()
        for point in points:
            print(point)
            lng, lat = point.coordinates[0], point.coordinates[1]
            location_names.append(gmaps.reverse_geocode((lat, lng), result_type="street_address")[0]["formatted_address"])
        return {"location_names": location_names}
    
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


