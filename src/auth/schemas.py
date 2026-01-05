from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None

class UserRegistration:
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
