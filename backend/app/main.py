
from datetime import datetime, timezone

from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes.cases import router as cases_router

app = FastAPI(
    title="Compliance Copilot API",
    description="KYC and AML case review assistant",
    version="0.4.0",
)

# Create database tables if they do not exist.
Base.metadata.create_all(bind=engine)

app.include_router(cases_router)


@app.get("/")
def root():
    return {
        "app": "Compliance Copilot",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
