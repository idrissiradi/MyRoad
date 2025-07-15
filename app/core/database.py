from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool


DATABASE_URL = "sqlite:///./database.db"

# Create engine with SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
