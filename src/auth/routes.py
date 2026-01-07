from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.main import get_db
from src.auth.dependencies import registration, login
from src.auth.schemas import UserRegistration, UserResponse, Token
from fastapi.security import OAuth2PasswordRequestForm


auth_routes = APIRouter()


@auth_routes.post('/', response_model=UserResponse)
def register(task: UserRegistration, db: Session = Depends(get_db)):
    return registration(task, db)
@auth_routes.post('/login', response_model=Token)
def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
