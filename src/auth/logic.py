from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from src.auth.models import User
from datetime import datetime, timedelta, timezone
import jwt
from src.config import Config
#-----------------------------------------------------------------------------------------------------------------------#

password_hash = PasswordHash.recommended()

def verify_password(plane_password: str, hashed_password: str):
    return password_hash.verify(plane_password, hashed_password)

def get_pass_hash(password: str):
    return password_hash.hash(password)

def get_user(db : Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return None
    return user
    # exp+ time
def create_access_token(data: dict, expire_delta: timedelta | None = None):
    if "sub" not in data:
        raise ValueError("Token payload must include 'sub'")

    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)