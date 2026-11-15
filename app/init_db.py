from app.database import client
from app.models.indexes import create_indexes


def initialize_database():
    try:
        # Verify MongoDB connection
        client.admin.command("ping")

        # Create database indexes
        create_indexes()

        print("Database initialized successfully!")

    except Exception as e:
        print("Database initialization failed:", e)
        raise