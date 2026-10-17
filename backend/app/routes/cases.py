
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case
from app.schemas.case import CaseCreate, CaseResponse, CaseUpdate

router = APIRouter(prefix="/cases", tags=["Cases"])


def get_missing_information(case: Case) -> list[str]:
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
        "created_at": case.created_at,
        "updated_at": case.updated_at,
        "missing_information": get_missing_information(case),
    }


@router.get("/", response_model=list[CaseResponse])
def get_cases(db: Session = Depends(get_db)):
    cases = db.query(Case).order_by(Case.created_at.desc()).all()
    return [serialize_case(case) for case in cases]


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found.",
        )

    return serialize_case(case)


@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(case_data: CaseCreate, db: Session = Depends(get_db)):
    new_case = Case(
        id=str(uuid4()),
        **case_data.model_dump(),
    )

    try:
        db.add(new_case)
        db.commit()
        db.refresh(new_case)
    except Exception:
        db.rollback()
        raise

    return serialize_case(new_case)


@router.patch("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: str,
    case_data: CaseUpdate,
    db: Session = Depends(get_db),
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found.",
        )

    updates = case_data.model_dump(exclude_unset=True)

    for field in ("client_name", "client_type", "status"):
        if field in updates and updates[field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{field} cannot be null.",
            )

    for field, value in updates.items():
        setattr(case, field, value)

    try:
        db.commit()
        db.refresh(case)
    except Exception:
        db.rollback()
        raise

    return serialize_case(case)


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: str, db: Session = Depends(get_db)):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found.",
        )

    try:
        db.delete(case)
        db.commit()
    except Exception:
        db.rollback()
        raise
