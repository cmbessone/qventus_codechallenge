import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.part_model import Part


def test_create_part(client: TestClient, test_db: Session):
    """Test creating a new part"""
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    response = client.post("/parts/", json=part_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == part_data["name"]
    assert data["sku"] == part_data["sku"]
    assert "id" in data

    # Verify database storage
    db_part = test_db.query(Part).filter(Part.id == data["id"]).first()
    assert db_part._is_active == 1  # Verify integer storage


def test_create_part_duplicate_sku(client: TestClient, test_db: Session):
    """Test creating a part with duplicate SKU"""
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    # Create first part
    client.post("/parts/", json=part_data)

    # Try to create second part with same SKU
    response = client.post("/parts/", json=part_data)
    assert response.status_code == 400  # Assuming you handle duplicate SKUs


def test_get_parts(client: TestClient, test_db: Session):
    """Test getting all parts"""
    # First create a part
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    client.post("/parts/", json=part_data)

    # Then get all parts
    response = client.get("/parts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_part(client: TestClient, test_db: Session):
    """Test getting a specific part"""
    # First create a part
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    create_response = client.post("/parts/", json=part_data)
    part_id = create_response.json()["id"]

    # Then get the specific part
    response = client.get(f"/parts/{part_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == part_id
    assert data["name"] == part_data["name"]


def test_update_part(client: TestClient, test_db: Session):
    """Test updating a part"""
    # First create a part
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    create_response = client.post("/parts/", json=part_data)
    part_id = create_response.json()["id"]

    # Then update it
    update_data = {
        "name": "Updated Part",
        "sku": "TEST001",
        "description": "An updated test part",
        "weight_ounces": 15,
        "is_active": True,
    }
    response = client.put(f"/parts/{part_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["weight_ounces"] == update_data["weight_ounces"]


def test_delete_part(client: TestClient, test_db: Session):
    """Test deleting a part"""
    # First create a part
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    create_response = client.post("/parts/", json=part_data)
    part_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/parts/{part_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/parts/{part_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_part(client: TestClient, test_db: Session):
    """Test getting a part that doesn't exist"""
    response = client.get("/parts/99999")
    assert response.status_code == 404


def test_update_nonexistent_part(client: TestClient, test_db: Session):
    """Test updating a part that doesn't exist"""
    update_data = {
        "name": "Updated Part",
        "sku": "TEST001",
        "description": "An updated test part",
        "weight_ounces": 15,
        "is_active": True,
    }
    response = client.put("/parts/99999", json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_part(client: TestClient, test_db: Session):
    """Test deleting a part that doesn't exist"""
    response = client.delete("/parts/99999")
    assert response.status_code == 404


def test_create_part_invalid_data(client: TestClient, test_db: Session):
    """Test creating a part with invalid data"""
    invalid_data = {
        "name": "Test Part",
        "sku": "TEST001",
        # Missing required fields
    }
    response = client.post("/parts/", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_update_part_sku(client: TestClient, test_db: Session):
    """Test updating a part's SKU"""
    # First create a part
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    create_response = client.post("/parts/", json=part_data)
    part_id = create_response.json()["id"]

    # Then update its SKU
    update_data = {
        "name": "Test Part",
        "sku": "TEST002",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    response = client.put(f"/parts/{part_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == update_data["sku"]


def test_part_inactive(client: TestClient, test_db: Session):
    """Test creating and updating inactive parts"""
    # Create an inactive part
    part_data = {
        "name": "Inactive Part",
        "sku": "TEST001",
        "description": "An inactive test part",
        "weight_ounces": 10,
        "is_active": False,
    }
    response = client.post("/parts/", json=part_data)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False

    # Update to active
    update_data = {
        "name": "Inactive Part",
        "sku": "TEST001",
        "description": "An inactive test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    response = client.put(f"/parts/{data['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is True


def test_create_part_inactive(client: TestClient, test_db: Session):
    """Test creating an inactive part"""
    part_data = {
        "name": "Inactive Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": False,
    }
    response = client.post("/parts/", json=part_data)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False

    # Verify database storage
    db_part = test_db.query(Part).filter(Part.id == data["id"]).first()
    assert db_part._is_active == 0  # Verify integer storage


def test_update_part_active_status(client: TestClient, test_db: Session):
    """Test updating part active status"""
    # Create an inactive part
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": False,
    }
    create_response = client.post("/parts/", json=part_data)
    part_id = create_response.json()["id"]

    # Verify initial state
    test_db.refresh(test_db.query(Part).filter(Part.id == part_id).first())
    db_part = test_db.query(Part).filter(Part.id == part_id).first()
    assert db_part._is_active == 0

    # Update to active
    update_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    response = client.put(f"/parts/{part_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is True

    # Verify database update
    test_db.refresh(test_db.query(Part).filter(Part.id == part_id).first())
    db_part = test_db.query(Part).filter(Part.id == part_id).first()
    assert db_part._is_active == 1


def test_part_active_status_conversion(client: TestClient, test_db: Session):
    """Test the conversion between boolean and integer for active status"""
    # Create a part
    part_data = {
        "name": "Test Part",
        "sku": "TEST001",
        "description": "A test part",
        "weight_ounces": 10,
        "is_active": True,
    }
    response = client.post("/parts/", json=part_data)
    part_id = response.json()["id"]

    # Get the part from database
    db_part = test_db.query(Part).filter(Part.id == part_id).first()

    # Test property getter
    assert db_part.is_active is True
    assert db_part._is_active == 1

    # Test property setter
    db_part.is_active = False
    assert db_part._is_active == 0
    test_db.commit()

    # Verify the change persisted
    db_part = test_db.query(Part).filter(Part.id == part_id).first()
    assert db_part._is_active == 0
    assert db_part.is_active is False
