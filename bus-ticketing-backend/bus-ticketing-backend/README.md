# Bus Ticketing Backend

A FastAPI + SQLAlchemy backend for managing bus ticket sales.

## Stack
- **FastAPI** – async REST API
- **SQLAlchemy 2** – ORM
- **Alembic** – DB migrations
- **PostgreSQL** – primary database
- **JWT** – stateless auth (python-jose + passlib/bcrypt)

## Quick Start

```bash
cd bus-ticketing-backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit with your credentials
alembic upgrade head
uvicorn app.main:app --reload
```

API docs → http://localhost:8000/docs

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret (keep private!) |
| `ALGORITHM` | JWT algorithm (default HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes |
