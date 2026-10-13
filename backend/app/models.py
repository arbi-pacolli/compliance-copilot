
from datetime import datetime, timezone

from sqlalchemy import DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    client_name: Mapped[str] = mapped_column(String(120), nullable=False)
    client_type: Mapped[str] = mapped_column(String(20), nullable=False)

    occupation: Mapped[str | None] = mapped_column(String(120), nullable=True)
    account_purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_activity: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_of_funds: Mapped[str | None] = mapped_column(Text, nullable=True)

    documents: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    screening_results: Mapped[str | None] = mapped_column(Text, nullable=True)
    transaction_context: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
