from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.models.base import Base


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def migrate_schema() -> None:
    """Apply small schema updates that are safe to run repeatedly."""
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS role VARCHAR(20)
                NOT NULL DEFAULT 'client'
                """
            )
        )

        connection.execute(
            text(
                """
                UPDATE users
                SET role = 'admin'
                WHERE LOWER(email) = 'pine12@mail.com'
                """
            )
        )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
