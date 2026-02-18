import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.storage import courses

client = TestClient(app)


# Reset storage before each test
@pytest.fixture(autouse=True)
def clear_courses():
    courses.clear()


# Public Access Test
def test_get_all_courses_empty():
    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == []


def test_get_course_by_id_not_found():
    response = client.get("/courses/999")
    assert response.status_code == 404


# Admin Create Course
def test_admin_create_course_success():
    response = client.post("/courses", json={
        "title": "Mathematics",
        "code": "MTH101",
        "role": "admin"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mathematics"
    assert data["code"] == "MTH101"
    assert data["id"] == 1


def test_student_cannot_create_course():
    response = client.post("/courses", json={
        "title": "Physics",
        "code": "PHY101",
        "role": "student"
    })

    assert response.status_code == 403


def test_create_course_missing_title():
    response = client.post("/courses", json={
        "title": "",
        "code": "MTH101",
        "role": "admin"
    })

    assert response.status_code == 422


def test_create_course_duplicate_code():
    client.post("/courses", json={
        "title": "Math",
        "code": "MTH101",
        "role": "admin"
    })

    response = client.post("/courses", json={
        "title": "Advanced Math",
        "code": "MTH101",
        "role": "admin"
    })

    assert response.status_code == 400
    assert "unique" in response.json()["detail"].lower()


# Admin Update Course
def test_admin_update_course_success():
    client.post("/courses", json={
        "title": "Math",
        "code": "MTH101",
        "role": "admin"
    })

    response = client.put("/courses/1", json={
        "title": "Advanced Math",
        "code": "MTH201",
        "role": "admin"
    })

    assert response.status_code == 200
    assert response.json()["title"] == "Advanced Math"


def test_student_cannot_update_course():
    client.post("/courses", json={
        "title": "Math",
        "code": "MTH101",
        "role": "admin"
    })

    response = client.put("/courses/1", json={
        "title": "Changed",
        "code": "MTH999",
        "role": "student"
    })

    assert response.status_code == 403


# Admin Delete Course
def test_admin_delete_course_success():
    client.post("/courses", json={
        "title": "Math",
        "code": "MTH101",
        "role": "admin"
    })

    response = client.request("DELETE", "/courses/1", json={
        "role": "admin"
    })

    assert response.status_code == 200
    assert len(courses) == 0


def test_student_cannot_delete_course():
    client.post("/courses", json={
        "title": "Math",
        "code": "MTH101",
        "role": "admin"
    })

    response = client.request("DELETE", "/courses/1", json={
        "role": "student"
    })

    assert response.status_code == 403
