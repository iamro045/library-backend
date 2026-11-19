
from fastapi import APIRouter, Depends

from app.models.collections import (
    books_collection,
    members_collection
)

from app.services.auth_dependencies import require_librarian_or_admin


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(
    current_staff=Depends(require_librarian_or_admin)
):

    inventory_filter = {
        "book_id": {
            "$exists": True,
            "$nin": [None, "TEST001"]
        },
        "is_active": {"$ne": False}
    }

    total_books = books_collection.count_documents(
        inventory_filter
    )

    available_books = books_collection.count_documents({
        **inventory_filter,
        "status": "available"
    })

    issued_books = books_collection.count_documents({
        **inventory_filter,
        "status": "issued"
    })

    total_members = members_collection.count_documents({})

    return {
        "total_books": total_books,
        "available_books": available_books,
        "issued_books": issued_books,
        "total_members": total_members
    }
