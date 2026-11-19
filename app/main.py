
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables before importing routes and services
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.init_db import initialize_database
from app.routes.book_routes import router as book_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.staff_routes import router as staff_router
from app.routes.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database when application starts
    initialize_database()

    yield

    # Application shutdown
    print("Library API shutting down...")


app = FastAPI(
    title="Library Management System API",
    description="Backend API for LibraDesk",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(book_router)
app.include_router(staff_router)
app.include_router(auth_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "Library Management System API is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "LibraDesk"
    }
