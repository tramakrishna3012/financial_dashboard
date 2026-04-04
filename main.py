from fastapi import FastAPI
from database import engine, Base
from routes import user, record, dashboard

# 1. Initialize Tables (SQLite database will be created if not exists)
Base.metadata.create_all(bind=engine)

# 2. Main Application Instance
app = FastAPI(
    title="Finance Dashboard Project",
    description="A beginner-friendly Backend for managing financial records.",
    version="1.0.0"
)

# 3. Include Sub-Routers
app.include_router(user.router)
app.include_router(record.router)
app.include_router(dashboard.router)

# 4. Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Finance Dashboard System API!"}

# =====================================================================
# README / TEST INSTRUCTIONS
# =====================================================================
"""
HOW TO RUN:
1. Open terminal and navigate to the project folder.
2. Install dependencies:
   pip install fastapi pydantic sqlalchemy uvicorn
3. Run the development server:
   uvicorn main:app --reload
4. Open the documentation in your browser:
   http://127.0.0.1:8000/docs
   
HOW TO TEST (Using the /docs Swagger UI):
1. Create an Admin User (Using /users POST endpoint):
   Body -> { "name": "Admin", "email": "admin@test.com", "role": "admin" }

2. Create an Analyst User:
   Body -> { "name": "Alice", "email": "analyst@test.com", "role": "analyst" }

3. Create a Financial Record (Admin only route):
   - Click "Try it out" 
   - Add Header "x-user-email: admin@test.com"
   - Body -> { "user_id": 1, "amount": 1000, "type": "income", "category": "Salary", "date": "2024-01-01" }

4. Get Dashboard Summary (Analyst or Admin):
   - Add Header "x-user-email: analyst@test.com"
   (Calling this route without header or without right role will result in 403 Forbidden Error!)
"""
