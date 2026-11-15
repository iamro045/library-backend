
from app.models.collections import (
    books_collection,
    book_copies_collection,
    members_collection,
    users_collection
)


def create_indexes():

    # Books
    books_collection.create_index(
        "book_id",
        unique=True
    )

    books_collection.create_index(
        "barcode",
        unique=True
    )

    books_collection.create_index("title")

    # Book copies - reserved for future functionality
    book_copies_collection.create_index(
        "barcode",
        unique=True
    )

    book_copies_collection.create_index("book_id")

    # Members - reserved for future functionality
    members_collection.create_index(
        "member_id",
        unique=True
    )

    # Users - reserved for future functionality
    users_collection.create_index(
        "username",
        unique=True
    )

    users_collection.create_index(
        "email",
        unique=True,
        partialFilterExpression={
            "email": {"$type": "string"}
        }
    )

    print("Database indexes created successfully!")
