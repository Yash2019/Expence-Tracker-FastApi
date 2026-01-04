from src.db.main import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        nullable=False
    )

    first_name: Mapped[str | None] = mapped_column(
        nullable=True
    )

    last_name: Mapped[str | None] = mapped_column(
        nullable=True
    )

    is_verified: Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )
