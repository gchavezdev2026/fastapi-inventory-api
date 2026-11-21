import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Restablece la base de datos de pruebas antes de cada test."""
    db.reset()
    db._seed_data()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["documentation"] == "/docs"


def test_get_all_products():
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4


def test_filter_products_by_category():
    response = client.get("/api/v1/products/?category=Accesorios")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for item in data:
        assert item["category"] == "Accesorios"


def test_filter_products_by_price_range():
    response = client.get("/api/v1/products/?min_price=40.0&max_price=500.0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for item in data:
        assert 40.0 <= item["price"] <= 500.0


def test_search_products():
    response = client.get("/api/v1/products/?search=Mecánico")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Teclado Mecánico" in data[0]["name"]


def test_get_product_by_id_success():
    response = client.get("/api/v1/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Laptop Pro 15"


def test_get_product_by_id_not_found():
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Producto con ID 999 no encontrado"


def test_create_product_success():
    payload = {
        "name": "Silla Gaming Ergonómica",
        "description": "Silla reclinable con soporte lumbar",
        "price": 249.99,
        "stock": 12,
        "category": "Muebles"
    }
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 5
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]
    assert data["category"] == payload["category"]
    assert "created_at" in data
    assert "updated_at" in data


def test_create_product_validation_error_invalid_price():
    payload = {
        "name": "Producto Inválido",
        "description": "Prueba",
        "price": -10.0,
        "stock": 5,
        "category": "Pruebas"
    }
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code == 422


def test_create_product_validation_error_invalid_stock():
    payload = {
        "name": "Producto Inválido",
        "description": "Prueba",
        "price": 10.0,
        "stock": -5,
        "category": "Pruebas"
    }
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code == 422


def test_create_product_validation_error_missing_field():
    payload = {
        "description": "Falta el nombre y precio",
        "stock": 5,
        "category": "Pruebas"
    }
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code == 422


def test_update_product_success():
    payload = {
        "name": "Laptop Pro 16 Ultimate",
        "description": "Laptop actualizada de ultra rendimiento",
        "price": 1599.99,
        "stock": 8,
        "category": "Electrónica"
    }
    response = client.put("/api/v1/products/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]


def test_update_product_not_found():
    payload = {
        "name": "Producto Inexistente",
        "description": "Prueba",
        "price": 100.0,
        "stock": 10,
        "category": "Pruebas"
    }
    response = client.put("/api/v1/products/999", json=payload)
    assert response.status_code == 404


def test_patch_product_success():
    payload = {
        "price": 1199.99,
        "stock": 20
    }
    response = client.patch("/api/v1/products/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["price"] == 1199.99
    assert data["stock"] == 20
    assert data["name"] == "Laptop Pro 15"  # Mantiene los otros datos intactos


def test_patch_product_not_found():
    payload = {"price": 100.0}
    response = client.patch("/api/v1/products/999", json=payload)
    assert response.status_code == 404


def test_delete_product_success():
    response = client.delete("/api/v1/products/1")
    assert response.status_code == 204

    # Verificar que realmente fue eliminado
    get_response = client.get("/api/v1/products/1")
    assert get_response.status_code == 404


def test_delete_product_not_found():
    response = client.delete("/api/v1/products/999")
    assert response.status_code == 404
