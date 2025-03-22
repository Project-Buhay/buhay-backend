from fastapi import APIRouter, HTTPException, status

from models import RouteInfo
from routing.cache_database import route_info

router = APIRouter()

@router.post("/get_route_info", status_code=status.HTTP_200_OK)
async def get_route_info(route_id: RouteInfo):
    try:
        data = await route_info(route_id.route_id)
        return {"payload": data}
    
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