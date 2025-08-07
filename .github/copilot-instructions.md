# Copilot Instructions for Task Manager FastAPI Project

## Project Overview
This is a FastAPI-based backend for a Task Manager application. The codebase is organized for clarity and modularity, with distinct folders for models, routes, schemas, and services. The database layer uses SQLAlchemy for ORM and connection management.

## Architecture & Key Components
- **app/main.py**: FastAPI app entry point. Routers are registered here.
- **app/models/**: SQLAlchemy models (e.g., `user.py`).
- **app/routes/**: API route definitions. Each resource typically has its own file.
- **app/schemas/**: Pydantic schemas for request/response validation.
- **app/services/**: Business logic and service functions.
- **app/database.py**: SQLAlchemy engine/session setup. Connection string and session management are handled here.

## Developer Workflows
- **Environment**: Activate the virtual environment in `env/` before running or installing dependencies.
  - PowerShell: `./env/Scripts/Activate.ps1`
- **Install dependencies**: `pip install -r requirements.txt`
- **Run server**: `uvicorn app.main:app --reload`
- **Database migrations**: Not present by default; if using Alembic, add migration instructions here.

## Patterns & Conventions
- **Routes**: Use APIRouter in each file under `app/routes/`. Register routers in `main.py`.
- **Models**: SQLAlchemy models are defined in `app/models/` and imported as needed.
- **Schemas**: Pydantic schemas are in `app/schemas/`, used for request/response validation.
- **Services**: Business logic is separated into `app/services/` for maintainability.
- **Database**: Connection and session management are centralized in `app/database.py`.
- **Naming**: Use snake_case for files and variables, PascalCase for class names.

## External Dependencies
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **python-dotenv**: Environment variable management (if used)

## Integration Points
- **Database**: SQLAlchemy connects to the database using a connection string in `app/database.py`.
- **API**: All endpoints are defined in `app/routes/` and registered in `main.py`.

## Example Patterns
- Registering a router in `main.py`:
  ```python
  from app.routes import user
  app.include_router(user.router)
  ```
- Creating a SQLAlchemy model in `models/user.py`:
  ```python
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True, index=True)
      # ...
  ```
- Defining a Pydantic schema in `schemas/user.py`:
  ```python
  class UserCreate(BaseModel):
      username: str
      password: str
  ```

## Notes
- No test or migration framework is present by default.
- Add new dependencies to `requirements.txt` and install in the active environment.
- Keep business logic out of route files; use services for non-trivial operations.

---

_Review and update this file as the project evolves. If any section is unclear or missing, provide feedback for improvement._
