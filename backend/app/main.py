from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.core.config import Settings
from app.core.database import engine, create_db_and_tables
from app.api.v1 import auth, generate, payments, projects, credits

# Load environment variables
load_dotenv()

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    print("🚀 Orionix Builder API starting up...")
    yield
    # Shutdown
    print("👋 Orionix Builder API shutting down...")

app = FastAPI(
    title="Orionix Builder API",
    description="Next-generation AI Web Builder Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(generate.router, prefix="/api/v1", tags=["generate"])
app.include_router(payments.router, prefix="/api/v1", tags=["payments"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(credits.router, prefix="/api/v1", tags=["credits"])

@app.get("/")
async def root():
    return {"message": "Orionix Builder API", "status": "healthy", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orionix-builder"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
