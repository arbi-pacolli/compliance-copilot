
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case
from app.schemas.case import CaseCreate, CaseResponse, CaseUpdate

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get("/", response_model=list[CaseResponse])
def get_cases(db: Session = Depends(get_db)):
    return db.query(Case).order_by(Case.id.desc()).all()


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found.",
        )

    return case


@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(case_data: CaseCreate, db: Session = Depends(get_db)):
    existing_case = (
        db.query(Case)
        .filter(Case.case_reference == case_data.case_reference)
        .first()
    )

    if existing_case:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A case with this reference already exists.",
        )

    new_case = Case(**case_data.model_dump())
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case


@router.patch("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: int,
    case_data: CaseUpdate,
    db: Session = Depends(get_db),
):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found.",
        )

    updates = case_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(case, field, value)

    db.commit()
    db.refresh(case)

    return case


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found.",
        )

    db.delete(case)
    db.commit()
