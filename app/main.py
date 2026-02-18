from fastapi import FastAPI
from app.api.v1 import enrollments, users, courses

app = FastAPI(
    title="Course Enrollment Management API",
    description="A simple API for managing course enrollments with role-based access control.",
    version="1.0.0"
)

app.include_router(enrollments.router)
app.include_router(users.router)
app.include_router(courses.router)

@app.get("/", status_code=200, tags=["Health"])
async def health_check():
    return {"status": "API is running"}