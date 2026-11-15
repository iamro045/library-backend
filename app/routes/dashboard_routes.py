
from fastapi import APIRouter
from app.models.collections import (
    books_collection,
    members_collection
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_dashboard_stats():

    # Exclude test records from actual library inventory
    inventory_filter = {
        "book_id": {
            "$exists": True,
            "$nin": [None, "TEST001"]
        }
    }

    # Total physical books
    total_books = books_collection.count_documents(
        inventory_filter
    )

    # Books by availability status
    available_books = books_collection.count_documents({
        **inventory_filter,
        "status": "available"
    })

    issued_books = books_collection.count_documents({
        **inventory_filter,
        "status": "issued"
    })

    # Registered library members
    total_members = members_collection.count_documents({})

    return {
        "total_books": total_books,
        "available_books": available_books,
        "issued_books": issued_books,
        "total_members": total_members
    }
