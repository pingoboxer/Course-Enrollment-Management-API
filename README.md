# 📘 Event Management & Enrollment API

A modern, modular backend system built with **FastAPI** that manages users, courses, and student enrollments.

This project demonstrates clean architecture principles, role-based access control, validation handling, and relationship management using in-memory storage.

---

## 🚀 Features

### 👤 User Management

* Create users (student/admin)
* Retrieve all users
* Retrieve a specific user by ID
* Email validation using Pydantic `EmailStr`
* Duplicate email prevention

### 📚 Course Management

* Admin-only course creation
* Update course details
* Delete course (with cascading enrollment cleanup)
* Prevent duplicate course codes
* Public course retrieval

### 🎓 Enrollment System

* Student enrollment into courses
* Duplicate enrollment prevention
* Student deregistration
* Admin force deregistration
* View student enrollments
* View course enrollments (admin)

---

## 🏗 Architecture & Design

This project follows a **layered architecture pattern**:


app/
│
├── core/            # Shared storage &configuration
|
├── schemas/          # Pydantic models (input/output validation)
|
├── services/           # Business logic layer
|
├── api/v1         # API endpoints (thin controllers)
|
└── main.py             # Application entry point


### 🔹 Separation of Concerns

| Layer   | Responsibility          |
| ------- | ----------------------- |
| Api/v1  | HTTP handling only      |
| Schema  | Input/output validation |
| Service | Business logic          |
| Storage | In-memory data store    |

This design ensures:

* Maintainability
* Testability
* Scalability
* Clean code organization

---

## 🧠 Design Decisions

### 1️⃣ Validation Strategy

* Format validation handled by **Pydantic schemas**
* Business rule validation handled by **Service layer**
* FastAPI automatically handles 422 errors for invalid inputs

### 2️⃣ Role-Based Access Control

Role is passed via request data and validated inside the service layer.

* `student` → Can enroll and deregister
* `admin` → Can manage courses and view all enrollments

### 3️⃣ Duplicate Prevention

* Email uniqueness enforced
* Course code uniqueness enforced
* Enrollment duplication prevented

### 4️⃣ Cascading Delete Logic

When a course is deleted:

* All related enrollments are automatically removed
* Prevents orphaned relationships

---

## 🧪 Testing

The project includes comprehensive test coverage using:

* `pytest`
* `FastAPI TestClient`

Test coverage includes:

* Success scenarios
* Role violations
* Duplicate prevention
* Invalid inputs
* Relationship integrity

Run tests:


pytest

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository


git clone <your-repo-url>
cd <project-folder>


### 2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows


### 3️⃣ Install Dependencies

pip install -r requirements.txt


### 4️⃣ Run the Server


uvicorn app.main:app --reload


## 📌 API Overview

### Users

POST   /users
GET    /users
GET    /users/{id}

### Courses


GET    /courses
GET    /courses/{id}
POST   /courses        (admin only)
PUT    /courses/{id}   (admin only)
DELETE /courses/{id}   (admin only)


### Enrollments


POST   /enrollments
DELETE /enrollments
GET    /enrollments/users/{user_id}
GET    /enrollments?role=admin
GET    /enrollments/courses/{course_id}?role=admin
DELETE /enrollments/admin


---

## 🛠 Technologies Used

* Python 3.10+
* FastAPI
* Pydantic
* Pytest
* Uvicorn

---

## 📈 Future Improvements

* Replace in-memory storage with PostgreSQL
* Implement JWT authentication
* Introduce dependency injection
* Add pagination & filtering
* Docker containerization
* CI/CD pipeline integration

---

## 🎯 Learning Outcomes

This project demonstrates:

* Clean service-layer architecture
* RESTful API design
* Role-based logic enforcement
* Defensive validation practices
* Test-driven thinking
* Relationship management without ORM

---

## 👨 Author

Raphael Kpamor
Backend Engineering Student
Passionate about scalable backend systems and clean architecture.
