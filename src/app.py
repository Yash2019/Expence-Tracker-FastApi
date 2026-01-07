from fastapi import FastAPI
from src.expence.routes import expence_router
from src.auth.routes import auth_routes
from src.db.main import create_table
app = FastAPI()
create_table()

app.include_router(
    auth_routes,
    prefix='/api/v1/auth',
    tags=['auth']
)


app.include_router(
    expence_router,
    prefix="/api/v1/expenses",
    tags=["expenses"]
)