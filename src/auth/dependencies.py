from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.auth.models import User
from src.auth.logic import get_user, get_pass_hash, authenticate_user, create_access_token
from src.auth.schemas import UserRegistration
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.db.main import get_db
from src.config import Config
#-----------------------------------------------------------------------------------------------------------------------#
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')
password_hash = PasswordHash.recommended()

def get_current_user(token: Annotated[str, Depends(oauth_scheme)],
                        db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user =get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user

def registration(user_create: UserRegistration, db: Session):
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    hashed_password = get_pass_hash(user_create.password)

    new_user = User(
        username=user_create.username,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        hashed_password=hashed_password,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(db: Session, username: str, password: str):
    user =  authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token(
        data=  {'sub': user.username}
    )

    return  {
        'access_token': access_token,
        'token_type': 'bearer'
    }
