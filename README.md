# Devinote

Devinote is a FastAPI backend for creating, organizing, and sharing personal notes. Users can register and authenticate, manage notes and labels, and share those resources with other users.

## Features

- User registration and JWT authentication
- Password hashing with `pwdlib`
- CRUD operations for notes
- Label creation and management
- Sharing notes and labels with other users
- SQLModel-based data models and repositories
- Database schema migrations with Alembic
- Interactive API documentation through FastAPI

## Technology stack

- **Python 3.14**
- **FastAPI** for the REST API
- **Uvicorn** and **Gunicorn** for serving the application
- **SQLModel** for typed SQL models and sessions
- **SQLAlchemy** as the database engine
- **PostgreSQL** with **Psycopg 3** as the production database driver
- **Alembic** for database migrations
- **Pydantic Settings** for configuration
- **PyJWT** for access tokens
- **pwdlib** and Argon2 support for password hashing
- **python-dotenv** for local environment files

## Project structure

```text
app/
├── api/routers/       API endpoints
├── core/              Configuration, database, and security
├── models/             SQLModel entities and schemas
├── repositories/       Database access layer
├── services/           Application and business logic
└── main.py             FastAPI application entry point
alembic/                Database migration environment and versions
requirements.txt        Python dependencies
```

## Requirements

- Python 3.14 or a compatible Python version
- PostgreSQL for deployment or production use
- A virtual environment is recommended

## Local setup

```bash
git clone https://github.com/ASPupiales99/blog-fastapi.git
cd devinote

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/devinote
JWT_SECRET=replace-with-a-long-random-secret
JWT_ALG=HS256
JWT_EXPIRE_MIN=1440
ENVIRONMENT=DEV
```

Run the migrations and start the development server:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`. FastAPI provides interactive documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database migrations

Apply existing migrations:

```bash
alembic upgrade head
```

Create a new migration after changing a model:

```bash
alembic revision --autogenerate -m "describe the schema change"
alembic upgrade head
```

## API overview

All application routes are prefixed with `/api/v1`.

| Area | Main routes |
| --- | --- |
| Authentication | `POST /auth/register`, `POST /auth/login`, `POST /auth/token` |
| Notes | `GET /note/`, `POST /note/`, `PATCH /note/{note_id}`, `DELETE /note/{note_id}` |
| Labels | `GET /labels/`, `POST /labels/`, `DELETE /labels/{label_id}` |
| Sharing | `POST` and `DELETE` routes under `/shares/notes/` and `/shares/labels/` |

Protected routes require a bearer token obtained from an authentication endpoint.

## Running in production

Configure the production environment with a PostgreSQL `DATABASE_URL`, a secure `JWT_SECRET`, and `ENVIRONMENT=PROD`. Run migrations as a release or deploy step, then start the application with a process manager such as:

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

The PostgreSQL URL is normalized to use the Psycopg 3 SQLAlchemy dialect (`postgresql+psycopg://`).
