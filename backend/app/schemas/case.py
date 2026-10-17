
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


CaseStatus = Literal["pending", "in_review", "completed"]
ClientType = Literal["individual", "business"]


class CaseCreate(BaseModel):
    client_name: str = Field(min_length=1, max_length=120)
    client_type: ClientType

    occupation: str | None = None
    account_purpose: str | None = None
    expected_activity: str | None = None
    source_of_funds: str | None = None

    documents: list[dict] = Field(default_factory=list)
    screening_results: str | None = None
    transaction_context: str | None = None

    status: CaseStatus = "pending"


class CaseUpdate(BaseModel):
    client_name: str | None = Field(default=None, min_length=1, max_length=120)
    client_type: ClientType | None = None

    occupation: str | None = None
    account_purpose: str | None = None
    expected_activity: str | None = None
    source_of_funds: str | None = None

    documents: list[dict] | None = None
    screening_results: str | None = None
    transaction_context: str | None = None

    status: CaseStatus | None = None


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    client_name: str
    client_type: str

    occupation: str | None
    account_purpose: str | None
    expected_activity: str | None
    source_of_funds: str | None

    documents: list[dict]
    screening_results: str | None
    transaction_context: str | None

    status: CaseStatus
    created_at: datetime
    updated_at: datetime
    missing_information: list[str] 