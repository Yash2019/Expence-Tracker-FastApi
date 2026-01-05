from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.auth.models import User
from datetime import datetime, timedelta, timezone
from src.auth.schemas import Token, TokenData
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.db.main import get_db
#-----------------------------------------------------------------------------------------------------------------------#

SECRET_KEY = 'veryverystrongpassword'
ALGORITHM = 'HS256'

oauth_scheme = OAuth2PasswordBearer(tokenUrl='Token')
password_hash = PasswordHash.recommended()

def verify_password(plane_password: str, hashed_password: str):
    return password_hash.verify(plane_password, hashed_password)

def get_pass_hash(password: str):
    return password_hash.hash(password)

def get_user(db : Session, username: str):
    if username in db:
        return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
# exp+ time
def create_access_token(data: dict, expire_delta: timedelta | None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Token = Annotated[str, Depends(oauth_scheme)],
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data =TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Annotated[User, Depends(get_current_user())]):
    if current_user.is_verified:
        raise HTTPException(status_code=404)
    return current_user


