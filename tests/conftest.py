import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.database import Base
from app.main import app
from app.database import get_db

# Use an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///file::memory:?cache=shared"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def clean_database(test_engine):
    """Clean the database between tests"""
    with test_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f"DELETE FROM {table.name}"))
        conn.commit()
    yield


@pytest.fixture
def test_db(test_session_factory):
    session = test_session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(test_session_factory):
    def override_get_db():
        try:
            db = test_session_factory()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_something(test_db: Session):
    # Use test_db for database operations
    pass


def test_api_endpoint(client: TestClient):
    # Use client for API requests
    response = client.post("/your-endpoint", json={"data": "value"})
    assert response.status_code == 200
