
from openpyxl import load_workbook
from app.models.collections import books_collection
from pymongo.errors import BulkWriteError


EXCEL_FILE = "data/Gayatri_BookNo_Barcode(1).xlsx"


def preview_excel_import():

    workbook = load_workbook(
        EXCEL_FILE,
        data_only=True
    )

    sheet = workbook["Book Catalog"]

    records = []
    seen_ids = set()

    for row in sheet.iter_rows(
        min_row=3,
        min_col=2,
        max_col=7,
        values_only=True
    ):

        book_id, title, author, publication, price, barcode = row

        if not book_id or not title:
            continue

        book_id = str(book_id).strip()

        if book_id in seen_ids:
            continue

        seen_ids.add(book_id)

        records.append({
            "book_id": book_id,
            "title": str(title).strip(),
            "author": str(author).strip() if author else None,
            "publication": str(publication).strip() if publication else None,
            "price": float(price) if isinstance(price, (int, float)) else None,
            "barcode": book_id
        })

    workbook.close()

    return records


def import_books_from_excel():

    records = preview_excel_import()

    if not records:
        return {"message": "No valid records found"}

    existing_ids = {
        book["book_id"]
        for book in books_collection.find(
            {"book_id": {"$in": [r["book_id"] for r in records]}},
            {"book_id": 1}
        )
    }

    new_records = [
        record for record in records
        if record["book_id"] not in existing_ids
    ]

    if new_records:
        try:
            result = books_collection.insert_many(
                new_records,
                ordered=False
            )
            inserted_count = len(result.inserted_ids)

        except BulkWriteError as error:
            inserted_count = error.details.get("nInserted", 0)

    else:
        inserted_count = 0

    return {
        "total_valid_records": len(records),
        "already_in_database": len(existing_ids),
        "inserted": inserted_count,
        "skipped": len(records) - inserted_count
    }
