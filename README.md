
# Compliance Copilot

An AI-assisted KYC and AML compliance platform for managing client cases, tracking missing information, and supporting compliance review workflows.

## Current Features

- Create and manage KYC/AML cases
- Store case information using SQLite
- Retrieve and update cases through a REST API
- Track missing information and supporting documents
- Manage case statuses
- Explore API endpoints through interactive Swagger documentation

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JavaScript / Node.js frontend (in development)

## Running the Backend

From the `backend` directory, activate the virtual environment and start the API:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Open the API documentation at:

http://127.0.0.1:8000/docs

## Development Status

This project is under active development. Features and documentation will evolve as development continues.

## Security Notice

Use synthetic data for development and testing. Never commit credentials, environment secrets, production databases, or confidential client information.

## Disclaimer

Compliance Copilot is a development and learning project. It supports compliance workflows and does not replace professional judgment or formal compliance decisions.
