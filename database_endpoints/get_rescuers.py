from fastapi import APIRouter, HTTPException, status

from routing.cache_database import rescuers

router = APIRouter()

@router.post("/get_rescuers", status_code=status.HTTP_200_OK)
async def get_rescuers():
    try: 
        data = await rescuers()
        return {"rescuers": data}
    
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