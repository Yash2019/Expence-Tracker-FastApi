from fastapi import FastAPI
from src.expence.routes import expence_router

app = FastAPI()

app.include_router(
    expence_router,
    prefix="/api/v1/expenses",
    tags=["expenses"]
)
