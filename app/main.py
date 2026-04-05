from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import user, record, dashboard
import uvicorn
import os

# 1. Initialize Tables (SQLite database will be created if not exists)
Base.metadata.create_all(bind=engine)

# 2. Main Application Instance
app = FastAPI(
    title="Finance Dashboard API",
    description="A minimalist, beginner-friendly backend API for managing financial records and viewing analytical summaries.",
    version="1.1.0"
)

# 3. Middleware Configuration
# Standard CORS setup to allow frontend applications to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include Sub-Routers
app.include_router(user.router)
app.include_router(record.router)
app.include_router(dashboard.router)

# 4. Root Endpoint
@app.get("/", summary="Check API Health", description="Returns a simple welcome message to verify the API is running correctly.")
def read_root():
    return {"message": "Welcome to the Finance Dashboard System API!"}

# =====================================================================
# README / TEST INSTRUCTIONS
# =====================================================================
"""
HOW TO RUN locally:
    uvicorn main:app --reload

HOW TO TEST:
Visit http://127.0.0.1:8000/docs for the interactive Swagger UI.
"""

# 6. Deployment Start Command
# This allows the app to be run directly via `python main.py` or deployed dynamically
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
