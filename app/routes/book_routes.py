
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.book_schema import BookCreate, BookUpdate
from app.schemas.book_copy_schema import BookCopyCreate

from app.services.book_service import (
    create_book,
    get_all_books,
    get_book_by_id,
    update_book,
    delete_book
)

from app.services.book_copy_service import (
    create_book_copy,
    get_book_copy_by_barcode
)

from app.services.excel_import_service import import_books_from_excel

from app.services.auth_dependencies import (
    require_admin,
    require_librarian_or_admin
)


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# ADD BOOK
@router.post("/", status_code=201)
def add_book(
    book: BookCreate,
    current_staff=Depends(require_librarian_or_admin)
):
    try:
        return create_book(book)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


# GET ALL BOOKS
@router.get("/")
def list_books(
    current_staff=Depends(require_librarian_or_admin)
):
    return get_all_books()


# GET BOOK BY BARCODE
@router.get("/barcode/{barcode}")
def retrieve_book_by_barcode(
    barcode: str,
    current_staff=Depends(require_librarian_or_admin)
):
    book_copy = get_book_copy_by_barcode(barcode)

    if not book_copy:
        raise HTTPException(
            status_code=404,
            detail="Book copy not found for this barcode"
        )

    return book_copy


# IMPORT BOOKS FROM EXCEL - ADMIN ONLY
@router.post("/import-excel")
def import_excel_books(
    admin=Depends(require_admin)
):
    try:
        return import_books_from_excel()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Excel import failed"
        )


# ADD BOOK COPY
@router.post("/copies", status_code=201)
def add_book_copy(
    copy: BookCopyCreate,
    current_staff=Depends(require_librarian_or_admin)
):
    try:
        return create_book_copy(copy)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# UPDATE BOOK
@router.put("/{book_id}")
def edit_book(
    book_id: str,
    book: BookUpdate,
    current_staff=Depends(require_librarian_or_admin)
):
    try:
        result = update_book(book_id, book)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# DELETE BOOK - SOFT DELETE
@router.delete("/{book_id}")
def remove_book(
    book_id: str,
    current_staff=Depends(require_librarian_or_admin)
):
    try:
        result = delete_book(book_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# GET BOOK BY DATABASE ID
@router.get("/{book_id}")
def retrieve_book(
    book_id: str,
    current_staff=Depends(require_librarian_or_admin)
):
    book = get_book_by_id(book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book
