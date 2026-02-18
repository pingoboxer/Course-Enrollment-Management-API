import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.storage import users, courses, enrollments

client = TestClient(app)


# Reset storage before each test
@pytest.fixture(autouse=True)
def clear_storage():
    users.clear()
    courses.clear()
    enrollments.clear()


# Helper Functions
def create_student():
    return client.post("/users", json={
        "name": "Student One",
        "email": "student@example.com",
        "role": "student"
    })


def create_admin():
    return client.post("/users", json={
        "name": "Admin One",
        "email": "admin@example.com",
        "role": "admin"
    })


def create_course():
    return client.post("/courses", json={
        "title": "Mathematics",
        "code": "MTH101",
        "role": "admin"
    })


# Student Enrollment Test
def test_student_enroll_success():
    create_student()
    create_course()

    response = client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    assert response.status_code == 201
    assert len(enrollments) == 1


def test_admin_cannot_enroll():
    create_admin()
    create_course()

    response = client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "admin"
    })

    assert response.status_code == 403


def test_enroll_nonexistent_student():
    create_course()

    response = client.post("/enrollments", json={
        "user_id": 999,
        "course_id": 1,
        "role": "student"
    })

    assert response.status_code == 404


def test_enroll_nonexistent_course():
    create_student()

    response = client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 999,
        "role": "student"
    })

    assert response.status_code == 404


def test_duplicate_enrollment_fails():
    create_student()
    create_course()

    client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    response = client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    assert response.status_code == 400


# Student Deregistration
def test_student_deregister_success():
    create_student()
    create_course()

    client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    response = client.request("DELETE", "/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    assert response.status_code == 200
    assert len(enrollments) == 0


def test_deregister_nonexistent_enrollment():
    create_student()
    create_course()

    response = client.request("DELETE", "/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    assert response.status_code == 404


# Student views of enrollments
def test_get_student_enrollments():
    create_student()
    create_course()

    client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    response = client.get("/users/1/enrollments")

    assert response.status_code == 200
    assert len(response.json()) == 1


# Admin View & Manage Enrollments
def test_admin_get_all_enrollments():
    create_student()
    create_course()

    client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    response = client.get("/enrollments", params={"role": "admin"})

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_admin_get_course_enrollments():
    create_student()
    create_course()

    client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    response = client.get("/courses/1/enrollments", params={"role": "admin"})

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_admin_force_deregister():
    create_student()
    create_course()

    client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })

    response = client.request("DELETE", "/admin/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "admin"
    })

    assert response.status_code == 200
    assert len(enrollments) == 0
