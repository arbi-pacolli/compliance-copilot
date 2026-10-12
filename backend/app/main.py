
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes.cases import router as cases_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Compliance Copilot API",
    description="Backend API for the Compliance Copilot application.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(cases_router)


@app.get("/")
def root():
    return {"message": "Compliance Copilot API is running."}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
