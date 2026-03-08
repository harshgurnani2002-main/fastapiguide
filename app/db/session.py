from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

# In order to use SQLite with FastAPI asynchronously or with multiple threads,
# we need to disable the check_same_thread requirement.
# This prevents errors when a database connection is created in one thread
# but accessed in another.
# We also use StaticPool here for SQLite to keep the database in-memory for testing,
# or to share the single connection across threads to avoid file locking issues
# that can happen with SQLite in production-like environments.
#
# IMPORTANT: For a truly production-grade app with high concurrency, you'd
# typically use PostgreSQL. But to make SQLite "production-grade" we add these args.
engine_args = {
    "connect_args": {"check_same_thread": False},
    "poolclass": StaticPool
} if settings.DATABASE_URL.startswith("sqlite") else {}

# Create the SQLAlchemy engine. The engine is the central object that provides
# connectivity to the database.
engine = create_engine(settings.DATABASE_URL, **engine_args)

# Create a customized Session class. We'll use this factory to create 
# new Session objects for each request.
# - autocommit=False: We manually control when to commit changes.
# - autoflush=False: Prevents SQLAlchemy from automatically saving changes
#   before we execute queries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
