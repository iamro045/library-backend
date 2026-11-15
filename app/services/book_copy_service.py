from app.models.collections import (
    books_collection,
    book_copies_collection
)
from app.schemas.book_copy_schema import BookCopyCreate
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


def create_book_copy(copy: BookCopyCreate):

    if not ObjectId.is_valid(copy.book_id):
        raise ValueError("Invalid book ID")

    book = books_collection.find_one({
        "_id": ObjectId(copy.book_id)
    })

    if not book:
        raise ValueError("Book not found")

    copy_data = copy.model_dump()
    copy_data["book_id"] = ObjectId(copy.book_id)

    try:
        result = book_copies_collection.insert_one(copy_data)

        return {
            "message": "Book copy added successfully",
            "copy_id": str(result.inserted_id)
        }

    except DuplicateKeyError:
        raise ValueError("This barcode already exists")



def get_book_copy_by_barcode(barcode: str):
    # First, search registered physical book copies
    copy = book_copies_collection.find_one({"barcode": barcode})

    if copy:
        book = books_collection.find_one({
            "_id": ObjectId(copy["book_id"])
        })

        if not book:
            return None

        return {
            "copy_id": str(copy["_id"]),
            "book_id": str(book["_id"]),
            "barcode": copy.get("barcode"),
            "status": copy.get("status", "available"),
            "shelf_location": copy.get("shelf_location"),
            "title": book.get("title"),
            "author": book.get("author"),
            "publication": book.get("publication") or book.get("publisher"),
            "price": book.get("price")
        }

    # If not found, search the main book catalogue
    book = books_collection.find_one({
        "$or": [
            {"barcode": barcode},
            {"book_id": barcode},
            {"isbn": barcode}
        ]
    })

    if not book:
        return None

    return {
        "copy_id": None,
        "book_id": str(book["_id"]),
        "barcode": book.get("barcode") or barcode,
        "status": "not_registered",
        "shelf_location": None,
        "title": book.get("title"),
        "author": book.get("author"),
        "publication": book.get("publication") or book.get("publisher"),
        "price": book.get("price")
    }
