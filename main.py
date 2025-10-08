from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routers import auth, users, birthdays, contributions, gifts
from starlette.config import Config
from db.database import SessionLocal, Base, engine
from factories import TestDataSeeder
from sqlalchemy.orm import Session

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

# Create tables
Base.metadata.create_all(bind=engine)

# Seed database
def seed_db():
    db: Session = SessionLocal()
    try:
        # Check if users exist to avoid duplicate seeding
        from models.users import User
        user_count = db.query(User).count()
        if user_count == 0:
            print("🌱 Seeding database with test data...")
            TestDataSeeder.seed_complete_scenario(db)
            print("✅ Database seeded!")
        else:
            print("ℹ️ Database already has data. Skipping seed.")
    finally:
        db.close()

# Call seeding function
seed_db()

app.include_router(auth.router, prefix='/auth')
app.include_router(users.router)
app.include_router(birthdays.router)
app.include_router(contributions.router)
app.include_router(gifts.router)

# This allows to serve the fastAPI application, uvicorn is a web-server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)