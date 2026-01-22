from fastapi import FastAPI
from app.api.v1 import auth, users

app = FastAPI(
  title="Workout Tracker API",
  description="API for managing workout routines and exercises",
  version="1.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Workout Tracker API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}