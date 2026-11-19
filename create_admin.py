
from pathlib import Path
from getpass import getpass

from dotenv import load_dotenv

# Load environment variables before importing application services
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from app.schemas.staff_schema import StaffCreate
from app.services.staff_service import (
    staff_collection,
    create_staff
)


def main():
    print("\n========== LibraDesk Admin Setup ==========\n")

    # Prevent accidental creation of multiple initial Admin accounts
    existing_admin = staff_collection.find_one({"role": "admin"})

    if existing_admin:
        print("An Admin account already exists.")
        print("No new Admin account was created.")
        return

    full_name = input("Enter Admin full name: ").strip()
    username = input("Enter Admin username: ").strip().lower()

    if not full_name or not username:
        print("Name and username cannot be empty.")
        return

    password = getpass("Enter Admin password: ")
    confirm_password = getpass("Confirm Admin password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    try:
        admin_data = StaffCreate(
            full_name=full_name,
            username=username,
            password=password,
            role="admin"
        )

        result = create_staff(admin_data)

        print("\nAdmin account created successfully!")
        print("Staff ID:", result["staff_id"])
        print("Username:", result["username"])
        print("Role: admin")

    except ValueError as error:
        print("\nError:", error)

    except Exception as error:
        print("\nUnexpected error:", error)


if __name__ == "__main__":
    main()
