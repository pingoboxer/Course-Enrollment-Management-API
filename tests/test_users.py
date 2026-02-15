import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.storage import users

client = TestClient(app)


# Reset storage before each test
@pytest.fixture(autouse=True)
def clear_users():
    users.clear()


# Create User Tests
def test_create_student_user_success():
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "role": "student"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["role"] == "student"
    assert data["id"] == 1


def test_create_admin_user_success():
    response = client.post("/users", json={
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "admin"
    })

    assert response.status_code == 201
    assert response.json()["role"] == "admin"


def test_create_user_invalid_email():
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "not-an-email",
        "role": "student"
    })

    assert response.status_code == 422  # Validation error


def test_create_user_invalid_role():
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "role": "teacher"
    })

    assert response.status_code == 422


def test_create_user_empty_name():
    response = client.post("/users", json={
        "name": "",
        "email": "john@example.com",
        "role": "student"
    })

    assert response.status_code == 422



# Get All Users
def test_get_all_users():
    client.post("/users", json={
        "name": "User One",
        "email": "user1@example.com",
        "role": "student"
    })

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 1


# Get User by ID
def test_get_user_by_id_success():
    client.post("/users", json={
        "name": "User One",
        "email": "user1@example.com",
        "role": "student"
    })

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["name"] == "User One"


def test_get_user_by_id_not_found():
    response = client.get("/users/999")

    assert response.status_code == 404
