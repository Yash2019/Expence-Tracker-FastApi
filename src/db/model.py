import uuid
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.db.main import Base

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)

    uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False,index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False
    )
    category: Mapped[str] = mapped_column(nullable=False)

    description: Mapped[str | None] = mapped_column(nullable=True)

    expense_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False
    )

