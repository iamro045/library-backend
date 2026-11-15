
from datetime import datetime, timezone

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.models.collections import books_collection
from app.schemas.book_schema import BookCreate, BookUpdate


# Actual library inventory filter.
# Excludes the two test records and soft-deleted books.
INVENTORY_FILTER = {
    "book_id": {
        "$exists": True,
        "$nin": [None, "TEST001"]
    },
    "is_active": {"$ne": False}
}


def create_book(book: BookCreate):
    try:
        book_data = book.model_dump()

        book_data["status"] = "available"
        book_data["is_active"] = True
        book_data["created_at"] = datetime.now(timezone.utc)

        result = books_collection.insert_one(book_data)

        return {
            "message": "Book added successfully",
            "book_id": book_data["book_id"],
            "database_id": str(result.inserted_id)
        }

    except DuplicateKeyError:
        raise ValueError("Book ID or barcode already exists")


def get_all_books():
    books = list(
        books_collection.find(INVENTORY_FILTER).sort("book_id", 1)
    )

    for book in books:
        book["_id"] = str(book["_id"])

    return books


def get_book_by_id(book_id: str):

    book = books_collection.find_one({
        "book_id": book_id.strip(),
        **INVENTORY_FILTER
    })

    if book:
        book["_id"] = str(book["_id"])

    return book


def get_book_by_barcode(barcode: str):
    book = books_collection.find_one({
        "barcode": barcode.strip(),
        **INVENTORY_FILTER
    })

    if book:
        book["_id"] = str(book["_id"])

    return book



def update_book(book_id: str, book_update: BookUpdate):
    book_id = book_id.strip()

    update_data = book_update.model_dump(exclude_unset=True)

    if not update_data:
        raise ValueError("No fields provided for update")

    try:
        result = books_collection.update_one(
            {
                "book_id": book_id,
                **INVENTORY_FILTER
            },
            {
                "$set": {
                    **update_data,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        if result.matched_count == 0:
            return None

        return {
            "message": "Book updated successfully",
            "book_id": book_id
        }

    except DuplicateKeyError:
        raise ValueError("Book ID or barcode already exists")


def delete_book(book_id: str):
    book_id = book_id.strip()

    book = books_collection.find_one({
        "book_id": book_id,
        **INVENTORY_FILTER
    })

    if not book:
        return None

    if book.get("status") == "issued":
        raise ValueError(
            "Cannot remove an issued book. Resolve its issue first."
        )

    books_collection.update_one(
        {"_id": book["_id"]},
        {
            "$set": {
                "is_active": False,
                "deleted_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "message": "Book removed from inventory successfully",
        "book_id": book_id
    }


def get_inventory_stats():
    return {
        "total_books": books_collection.count_documents(
            INVENTORY_FILTER
        ),
        "available_books": books_collection.count_documents({
            **INVENTORY_FILTER,
            "status": "available"
        }),
        "issued_books": books_collection.count_documents({
            **INVENTORY_FILTER,
            "status": "issued"
        }),
        "registered_members": 0
    }
