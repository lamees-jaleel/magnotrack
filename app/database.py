import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("magnotrack.database")

# Read DATABASE_URL from environment
# Default to Docker-Compose PostgreSQL connection for local development
RAW_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://magnotrack:magnotrack_secret@localhost:5432/magnotrack_db"
)

# Render and older platforms use "postgres://..." which SQLAlchemy 2.0 rejects.
# Standardize to "postgresql://"
if RAW_DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = RAW_DATABASE_URL

# Configure engine arguments depending on dialect
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Automatically reconnect dropped connections
    pool_recycle=300,    # Recycle connections after 5 minutes
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a database session and ensures closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> tuple[bool, str]:
    """Verify database connectivity by running a lightweight SELECT 1 query."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Database connection active"
    except Exception as exc:
        logger.error(f"Database connection error: {exc}")
        return False, str(exc)


def init_db():
    """Create all registered database tables if they do not exist."""
    import app.models  # ensure models are imported before creating tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
