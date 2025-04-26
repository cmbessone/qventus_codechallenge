from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)


def test_create_part():
    response = client.post(
        "/parts/",
        json={
            "name": "Test Part",
            "sku": f"SKU-{uuid.uuid4().hex[:6]}",
            "description": "Test description for this part",
            "weight_ounces": 5,
            "is_active": True,
        },
    )
    assert response.status_code == 200
    assert "sku" in response.json()


def test_get_parts():
    response = client.get("/parts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_top_words():
    response = client.get("/parts/top-words")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def create_dummy_part():
    response = client.post(
        "/parts/",
        json={
            "name": "Auto Test Part",
            "sku": f"SKU-{uuid.uuid4().hex[:6]}",
            "description": "Auto test desc",
            "weight_ounces": 10,
            "is_active": True,
        },
    )
    return response.json()


def test_update_part():
    part = create_dummy_part()
    response = client.put(
        f"/parts/{part['id']}",
        json={
            "name": "Updated Part",
            "sku": part["sku"],
            "description": "Updated desc",
            "weight_ounces": 20,
            "is_active": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Part"


def test_update_part_404():
    response = client.put(
        "/parts/99999",
        json={
            "name": "Missing",
            "sku": "MISSING999",
            "description": "not found",
            "weight_ounces": 5,
            "is_active": True,
        },
    )
    assert response.status_code == 404


def test_delete_part():
    part = create_dummy_part()
    response = client.delete(f"/parts/{part['id']}")
    assert response.status_code == 200


def test_delete_part_404():
    response = client.delete("/parts/99999")
    assert response.status_code == 404
