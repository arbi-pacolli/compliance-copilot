
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    case_reference: str = Field(min_length=1, max_length=50)
    client_name: str = Field(min_length=1, max_length=150)
    client_type: str = Field(min_length=1, max_length=50)
    review_purpose: str = Field(min_length=1, max_length=150)
    status: str = "Pending"
    risk_level: str = "Unassessed"
    missing_information: int = Field(default=0, ge=0)
    notes: str | None = None


class CaseUpdate(BaseModel):
    status: str | None = None
    risk_level: str | None = None
    missing_information: int | None = Field(default=None, ge=0)
    notes: str | None = None


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_reference: str
    client_name: str
    client_type: str
    review_purpose: str
    status: str
    risk_level: str
    missing_information: int
    notes: str | None
    created_at: datetime
