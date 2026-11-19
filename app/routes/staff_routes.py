
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.staff_schema import StaffCreate, StaffUpdate
from app.services.staff_service import (
    create_staff,
    get_all_staff,
    update_staff
)
from app.services.auth_dependencies import require_admin

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post("/", status_code=201)
def add_staff(
    staff: StaffCreate,
    admin=Depends(require_admin)
):
    try:
        if staff.role != "librarian":
            raise HTTPException(
                status_code=403,
                detail="Only Librarian accounts can be created through this endpoint"
            )

        return create_staff(staff)

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@router.get("/")
def list_staff(admin=Depends(require_admin)):
    return get_all_staff()


@router.patch("/{staff_id}")
def edit_staff(
    staff_id: str,
    staff_update: StaffUpdate,
    admin=Depends(require_admin)
):
    # Prevent Admin from deactivating or demoting their own account
    if staff_id == admin.get("staff_id"):
        if (
            staff_update.is_active is False
            or staff_update.role == "librarian"
        ):
            raise HTTPException(
                status_code=403,
                detail="You cannot deactivate or demote your own Admin account"
            )

    try:
        return update_staff(
            staff_id,
            staff_update.model_dump(exclude_unset=True)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
