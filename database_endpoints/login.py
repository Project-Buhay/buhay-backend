from fastapi import APIRouter, HTTPException, status

from models import LoginInput
from routing.cache_database import search_login

router = APIRouter()


@router.post("/login", status_code = status.HTTP_200_OK)
async def login(login_input: LoginInput):
    try:
        db_data = await search_login(login_input.username, login_input.password)
        
        # Valid
        if db_data: 
            return db_data

        # Invalid: Return person_id = 0, access_level = 0
        # since these cases are normally impossible.
        else:
            return {
                "person_id": 0,
                "access_control": 0
            }
        
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