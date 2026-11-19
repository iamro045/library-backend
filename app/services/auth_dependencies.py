
import os
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.models.collections import db


SECRET_KEY = os.getenv("LIBRADESK_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "LIBRADESK_SECRET_KEY environment variable is not configured"
    )

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

staff_collection = db["staff"]


def get_current_staff(token: str = Depends(oauth2_scheme)):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        staff_id = payload.get("sub")

        if not staff_id or not isinstance(staff_id, str):
            raise credentials_error

    except InvalidTokenError:
        raise credentials_error

    staff = staff_collection.find_one({
        "staff_id": staff_id,
        "is_active": True
    })

    if not staff:
        raise credentials_error

    return staff


def require_admin(current_staff=Depends(get_current_staff)):
    if current_staff.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_staff


def require_librarian_or_admin(
    current_staff=Depends(get_current_staff)
):
    if current_staff.get("role") not in {"admin", "librarian"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return current_staff
