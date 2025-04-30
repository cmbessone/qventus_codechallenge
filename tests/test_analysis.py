from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_top_words_empty(client: TestClient, test_db: Session):
    """Test top words analysis with no parts"""
    response = client.get("/parts/top-words")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_top_words_with_parts(client: TestClient, test_db: Session):
    """Test top words analysis with multiple parts"""
    # Create multiple parts with different descriptions
    parts_data = [
        {
            "name": "Part 1",
            "sku": "TEST001",
            "description": "A test part with common words",
            "weight_ounces": 10,
            "is_active": True,
        },
        {
            "name": "Part 2",
            "sku": "TEST002",
            "description": "Another test part with common words",
            "weight_ounces": 15,
            "is_active": True,
        },
        {
            "name": "Part 3",
            "sku": "TEST003",
            "description": "A third test part with common words",
            "weight_ounces": 20,
            "is_active": True,
        },
    ]

    for part in parts_data:
        client.post("/parts/", json=part)

    response = client.get("/parts/top-words")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Verify common words are present
    words = [item["word"] for item in data]
    assert "test" in words
    assert "part" in words
    assert "with" in words
    assert "common" in words
    assert "words" in words
