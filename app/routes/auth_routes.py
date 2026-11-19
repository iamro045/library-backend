
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from app.services.auth_service import (
    authenticate_staff,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def staff_login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    staff = authenticate_staff(
        form_data.username,
        form_data.password
    )

    if not staff:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(staff)

    return {
        "access_token": token,
        "token_type": "bearer",
        "staff": {
            "staff_id": staff["staff_id"],
            "full_name": staff["full_name"],
            "username": staff["username"],
            "role": staff["role"]
        }
    }
