
import os
import jwt

from datetime import datetime, timedelta, timezone

from app.services.staff_service import (
    get_staff_by_username,
    verify_password
)

SECRET_KEY = os.getenv("LIBRADESK_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "LIBRADESK_SECRET_KEY environment variable is not configured"
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_staff(username: str, password: str):
    staff = get_staff_by_username(username)

    if not staff:
        return None

    if not staff.get("is_active", False):
        return None

    if not verify_password(password, staff["password_hash"]):
        return None

    return staff


def create_access_token(staff: dict):
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": staff["staff_id"],
        "role": staff["role"],
        "exp": expires_at
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
