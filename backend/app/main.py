from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import Base
from app.database import engine

# Import every model explicitly.
# This registers all SQLAlchemy models and relationships.
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.match import JobMatch

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.resumes import router as resumes_router
from app.api.jobs import router as jobs_router
from app.api.dashboard import router as dashboard_router
from app.api.recommendations import router as recommendations_router
from app.api.matches import router as matches_router


app = FastAPI(
    title="CareerMatch AI",
    description="AI-powered career and job matching platform",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(
    bind=engine
)


@app.get(
    "/",
    tags=["default"],
)
def root():
    return {
        "message": "CareerMatch AI API is running"
    }


@app.get(
    "/health",
    tags=["default"],
)
def health_check():
    return {
        "status": "healthy"
    }


@app.get(
    "/health/database",
    tags=["default"],
)
def database_health_check():

    try:
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(
                text("SELECT 1")
            )

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }


app.include_router(
    auth_router
)

app.include_router(
    users_router
)

app.include_router(
    resumes_router
)

app.include_router(
    jobs_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    recommendations_router
)

app.include_router(
    matches_router
)
