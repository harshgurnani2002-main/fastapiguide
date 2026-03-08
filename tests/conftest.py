import os
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.base import Base
from app.main import app

# We override the DATABASE_URL here to use an in-memory SQLite database
# for blazing fast tests that don't mess up our dev/prod database.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create tests engine and sessionmaker
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def setup_test_db():
    """
    Session-scoped fixture to create the test database tables once.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db(setup_test_db) -> Generator:
    """
    Creates a fresh database session for a test.
    """
    connection = engine.connect()
    # We use a transaction so we can rollback after every test,
    # ensuring test isolation.
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    # Rollback constraints and close
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db) -> Generator:
    """
    TestClient fixture that overrides the get_db dependency to use the test db session above.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass # Session management is handled in the db fixture
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()
