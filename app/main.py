from fastapi import FastAPI
from app.api.v1 import enrollment

app = FastAPI()

app.include_router(enrollment.router)
