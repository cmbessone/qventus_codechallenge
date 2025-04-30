from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text


def test_database_connection(test_db: Session):
    """Test that we can connect to the test database"""
    result = test_db.execute(text("SELECT 1"))
    assert result.scalar() == 1


def test_api_client(client: TestClient):
    """Test that the test client is working"""
    response = client.get("/")
    # Depending on if root route exists
    assert response.status_code in (200, 404)
