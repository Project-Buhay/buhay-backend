from fastapi import APIRouter, HTTPException, status

from models import Assign
from routing.cache_database import assign_rescuer

router = APIRouter()

@router.post("/assign", status_code=status.HTTP_200_OK)
async def assign(input: Assign):
    try:
        success = await assign_rescuer(input.request_id, input.rescuer_id)
        return {"success": (success == input.request_id)}
    
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

