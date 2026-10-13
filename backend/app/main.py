
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Case

app = FastAPI(
    title="Compliance Copilot API",
    description="KYC and AML case review assistant",
    version="0.3.0",
)

# Create database tables if they do not exist.
Base.metadata.create_all(bind=engine)


class CaseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_name: str = Field(min_length=2, max_length=120)
    client_type: Literal["individual", "business"]
    occupation: str | None = Field(default=None, max_length=120)
    account_purpose: str | None = Field(default=None, max_length=500)
    expected_activity: str | None = Field(default=None, max_length=1000)
    source_of_funds: str | None = Field(default=None, max_length=500)
    documents: list[str] = Field(default_factory=list)
    screening_results: str | None = Field(default=None, max_length=1000)
    transaction_context: str | None = Field(default=None, max_length=1000)


class CaseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_name: str | None = Field(default=None, min_length=2, max_length=120)
    occupation: str | None = Field(default=None, max_length=120)
    account_purpose: str | None = Field(default=None, max_length=500)
    expected_activity: str | None = Field(default=None, max_length=1000)
    source_of_funds: str | None = Field(default=None, max_length=500)
    documents: list[str] | None = None
    screening_results: str | None = Field(default=None, max_length=1000)
    transaction_context: str | None = Field(default=None, max_length=1000)
    status: Literal["pending", "in_review", "completed"] | None = None


def missing_information(case: Case) -> list[str]:
    required_fields = {
        "occupation": "Occupation",
        "account_purpose": "Purpose of account",
        "expected_activity": "Expected activity",
        "source_of_funds": "Source of funds",
        "screening_results": "Screening results",
        "transaction_context": "Transaction context",
    }

    missing = [
        label
        for field, label in required_fields.items()
        if not getattr(case, field)
    ]

    if not case.documents:
        missing.append("Supporting documents")

    return missing


def serialize_case(case: Case) -> dict:
    return {
        "id": case.id,
        "client_name": case.client_name,
        "client_type": case.client_type,
        "occupation": case.occupation,
        "account_purpose": case.account_purpose,
        "expected_activity": case.expected_activity,
        "source_of_funds": case.source_of_funds,
        "documents": case.documents,
        "screening_results": case.screening_results,
        "transaction_context": case.transaction_context,
        "status": case.status,
        "created_at": case.created_at.isoformat(),
        "updated_at": case.updated_at.isoformat(),
        "missing_information": missing_information(case),
    }


@app.get("/")
def root():
    return {"app": "Compliance Copilot", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/cases/", status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    case = Case(
        id=str(uuid4()),
        **payload.model_dump(),
        status="pending",
        created_at=now,
        updated_at=now,
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return serialize_case(case)


@app.get("/cases/")
def list_cases(db: Session = Depends(get_db)):
    cases = db.scalars(select(Case).order_by(Case.created_at.desc())).all()
    return [serialize_case(case) for case in cases]


@app.get("/cases/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    return serialize_case(case)


@app.patch("/cases/{case_id}")
def update_case(
    case_id: str,
    payload: CaseUpdate,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null. Omit it if unchanged.",
            )
        setattr(case, field, value)

    case.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(case)

    return serialize_case(case)
