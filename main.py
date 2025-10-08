from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routers import auth, users, birthdays, contributions, gifts
from starlette.config import Config
from db.database import SessionLocal
from factories import TestDataSeeder

app = FastAPI(
    title="Symphony Birthday Planner",
    description="Internal symphony.is application for managing birthdays",
    version='0.1.0',
    docs_url='/docs',
    redoc_url='/redoc',
)

config = Config(".env")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Basically an allowance to make calls to the backend
app.add_middleware(
    SessionMiddleware,
    secret_key=config("SECRET_KEY"),
)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    from sqlalchemy import text
    # Optional check: only seed if empty
    user_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
    if user_count == 0:
        print("🌱 Seeding test data...")
        TestDataSeeder.seed_complete_scenario(db)
    db.close()

app.include_router(auth.router, prefix='/auth')
app.include_router(users.router)
app.include_router(birthdays.router)
app.include_router(contributions.router)
app.include_router(gifts.router)

# This allows to serve the fastAPI application, uvicorn is a web-server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)