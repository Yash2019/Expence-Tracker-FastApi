
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from datetime import datetime

class ExpenceCreate(BaseModel):
    amount: Decimal
    category: str
    description: str
    expense_date: datetime

class ExpenceRead(BaseModel):
    uuid: UUID
    amount: Decimal
    category: str
    description: str
    expense_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenceUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0)
    category: str | None = None
    description: str | None = None
    expense_date: datetime | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
