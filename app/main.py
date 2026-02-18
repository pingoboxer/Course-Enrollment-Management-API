from fastapi import FastAPI
from app.api.v1 import enrollments, users, courses

app = FastAPI()

app.include_router(enrollments.router)
app.include_router(users.router)
app.include_router(courses.router)

@app.get("/", status_code=200)
async def health_check():
    return {"status": "API is running"}