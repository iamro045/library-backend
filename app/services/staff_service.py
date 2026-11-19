
from datetime import datetime, timezone
from uuid import uuid4

from pymongo.errors import DuplicateKeyError
from pwdlib import PasswordHash

from app.models.collections import db

staff_collection = db["staff"]

# Ensure every username is unique
staff_collection.create_index("username", unique=True)

password_hash = PasswordHash.recommended()


def create_staff(staff_data):
    data = staff_data.model_dump()

    data["staff_id"] = str(uuid4())
    data["username"] = data["username"].strip().lower()
    data["full_name"] = data["full_name"].strip()

    data["password_hash"] = password_hash.hash(
        data.pop("password")
    )

    data["is_active"] = True
    data["created_at"] = datetime.now(timezone.utc)

    try:
        staff_collection.insert_one(data)

        return {
            "message": "Staff account created successfully",
            "staff_id": data["staff_id"],
            "username": data["username"]
        }

    except DuplicateKeyError:
        raise ValueError("Username already exists")


def get_all_staff():
    return list(
        staff_collection.find(
            {},
            {
                "_id": 0,
                "password_hash": 0
            }
        ).sort("full_name", 1)
    )


def get_staff_by_username(username):
    return staff_collection.find_one({
        "username": username.strip().lower()
    })


def get_staff_by_id(staff_id):
    return staff_collection.find_one({
        "staff_id": staff_id
    })


def verify_password(plain_password, hashed_password):
    return password_hash.verify(
        plain_password,
        hashed_password
    )


def update_staff(staff_id, update_data):
    staff = get_staff_by_id(staff_id)

    if not staff:
        raise ValueError("Staff account not found")

    # Only allow these fields to be updated
    allowed_fields = {"full_name", "role", "is_active"}

    updates = {
        key: value
        for key, value in update_data.items()
        if key in allowed_fields and value is not None
    }

    if not updates:
        raise ValueError("No valid fields provided for update")

    # Validate full name
    if "full_name" in updates:
        updates["full_name"] = updates["full_name"].strip()

        if len(updates["full_name"]) < 2:
            raise ValueError("Full name must contain at least 2 characters")

    # Validate role
    if "role" in updates:
        if updates["role"] not in {"admin", "librarian"}:
            raise ValueError("Invalid staff role")

    # Protect the last active Admin
    removing_admin = (
        staff["role"] == "admin"
        and staff.get("is_active", False)
        and (
            updates.get("role") == "librarian"
            or updates.get("is_active") is False
        )
    )

    if removing_admin:
        active_admin_count = staff_collection.count_documents({
            "role": "admin",
            "is_active": True
        })

        if active_admin_count <= 1:
            raise ValueError(
                "Cannot deactivate or demote the last active Admin"
            )

    updates["updated_at"] = datetime.now(timezone.utc)

    staff_collection.update_one(
        {"staff_id": staff_id},
        {"$set": updates}
    )

    updated_staff = get_staff_by_id(staff_id)

    updated_staff.pop("_id", None)
    updated_staff.pop("password_hash", None)

    return {
        "message": "Staff account updated successfully",
        "staff": updated_staff
    }
