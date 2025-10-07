# 🎻 Symphony Birthday Planner

This is the backend for the Birthday App, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, using **Alembic** for database migrations. The project is dockerized for easy development and deployment.

## Features

- User management (CRUD operations)
- Birthday and gift tracking
- Contributions management
- REST API ready to be consumed by the frontend

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker & Docker Compose

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/SymphoniousSara/back-end.git
cd back-end```

2. **Create a virtual environment (optional but recommended):**
```python -m venv .venv
source .venv/bin/activate

3. **Install dependencies:**
```pip install --upgrade pip
pip install -r requirements.txt

4. **Set up environment variables:**
Copy .env.example to .env and fill in your values.

5. **Start Docker containers and run migrations:**
```docker-compose up -d --build
docker-compose exec backend alembic upgrade head

6. **Run the backend locally (optional):**
```uvicorn main:app --reload --host 0.0.0.0 --port 8000`

7. **Common commands:**
```docker-compose exec backend alembic revision --autogenerate -m "migration_name"
docker-compose exec backend alembic upgrade head
docker-compose exec backend alembic downgrade -1
docker-compose exec db psql -U $POSTGRES_USER $POSTGRES_DB -c "\dt"





