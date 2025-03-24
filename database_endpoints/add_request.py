from fastapi import APIRouter, HTTPException, status

from models import AddRequestInput
from routing.cache_database import add_request_row
import googlemaps
from db_env import GOOGLE_MAPS_API

router = APIRouter()
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API)


@router.post("/add_request", status_code=status.HTTP_200_OK)
async def add_request(input: AddRequestInput):
    print(input)
    try:
        person_id: int = input.person_id
        raw_coordinates = list()
        coordinate_names = list()
        for point in input.coordinates:
            lng, lat = point.coordinates[0], point.coordinates[1]
            raw_coordinates.append({"coordinates": [lng, lat]})
            coordinate_names.append(
                gmaps.reverse_geocode((lat, lng), 
                    result_type="street_address|plus_code|premise|establishment|point_of_interest")
                    [0]["formatted_address"]
            )
        request_id = await add_request_row(person_id, raw_coordinates, coordinate_names)
        return {"request_id": request_id}

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
