from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

app = FastAPI(
    title="Symphony Birthday Planner",
    description="Internal symphony.is application for managing birthdays",
    version='0.1.0',
    docs_url='/docs',
    redoc_url='/redoc',
)

# Basically an allowance to make calls to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# This allows to serve the fastAPI application, uvicorn is a web-server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)