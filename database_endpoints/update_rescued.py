from fastapi import APIRouter, HTTPException, status

from models import UpdateRescued
from routing.cache_database import update_rescued_boolean

router = APIRouter()

@router.post("/update_rescued", status_code=status.HTTP_200_OK)
async def update_rescued(request_id: UpdateRescued):
    try:
        await update_rescued_boolean(request_id.request_id)
        return {"message": "done"}

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