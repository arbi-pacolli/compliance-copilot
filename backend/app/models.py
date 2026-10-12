
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    case_reference: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    client_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    client_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    review_purpose: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(30),
        default="Unassessed",
        nullable=False,
    )

    missing_information: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
