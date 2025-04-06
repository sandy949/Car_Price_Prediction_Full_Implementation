# project_root/backend/db.py

"""
db.py

This module sets up the database connection using SQLAlchemy with retry logic,
environment variable support, and a PostgreSQL backend. It includes connection pooling,
session creation, and base class declaration for ORM models.

Used in: Flask backend application with PostgreSQL and Alembic migrations.
"""

import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# If DATABASE_URL is defined (like in Docker), use it directly. Otherwise, construct it from parts.
DATABASE_URL = os.getenv("DATABASE_URL") or \
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Retry logic
def create_engine_with_retry(url, retries=5, delay=2):
    """
    Attempts to create a SQLAlchemy engine with retry logic.

    Args:
        url (str): The database URL for connection.
        retries (int, optional): Number of retries before giving up. Defaults to 5.
        delay (int, optional): Seconds to wait between retries. Defaults to 2.

    Returns:
        sqlalchemy.Engine: SQLAlchemy engine object connected to the database.

    Raises:
        Exception: If connection fails after the defined retries.
    """
    for attempt in range(1, retries + 1):
        try:
            engine = create_engine(
                url,
                pool_size=10,            # number of connections maintained
                max_overflow=20,         # additional connections allowed temporarily
                pool_timeout=30,         # seconds to wait before giving up
                pool_recycle=1800        # refresh connections after 30 minutes
            )
            # Test the connection
            with engine.connect() as connection:
                print("✅ Connected to DB!")
            return engine
        except OperationalError as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            time.sleep(delay)
    raise Exception("🔁 Could not connect to the database after several retries.")

# Create engine
engine = create_engine_with_retry(DATABASE_URL)

if __name__ == "__main__":
    from sqlalchemy import text

    # Simple query to test connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print("✅ PostgreSQL version:")
            for row in result:
                print(row)
    except Exception as e:
        print(f"❌ Failed to run test query: {e}")

from sqlalchemy.orm import declarative_base

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()