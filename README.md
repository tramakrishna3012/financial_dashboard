# Finance Dashboard System (Backend API)

Welcome to my backend project! This is a complete Python backend system built for a Finance Dashboard where users can manage their financial records. It includes Role-Based Access Control (RBAC) to ensure different users have the proper permissions to view and edit data.

## Tech Stack
- **Framework**: FastAPI (for building high-performance APIs)
- **Database**: SQLite (lightweight, file-based database, great for beginner projects)
- **ORM**: SQLAlchemy (to interact with the database using Python objects instead of raw SQL)
- **Validation**: Pydantic (to seamlessly validate JSON request bodies)

## Project Structure

To keep the application neat and easy to understand, the code is separated into dedicated files based on their responsibilities:

```text
finance_dashboard/
├── main.py          # The entry point of the app, connects routers and starts the server
├── database.py      # Database connection and engine setup
├── models.py        # SQLAlchemy classes (Database Tables: User, Record)
├── schemas.py       # Pydantic models for verifying JSON requests/responses
├── crud.py          # All database logic (Create, Read, Update, Delete commands)
├── dependencies.py  # Contains logic to handle permissions and Role-Based Access Control
└── routes/          # Our API endpoints logically separated by feature
    ├── user.py      
    ├── record.py    
    └── dashboard.py 
```

## Key Features Implemented

1. **User Management**: Create and list users. Users are assigned one of three roles (`viewer`, `analyst`, `admin`).
2. **Financial Records Management**: Add, view, update, and delete financial records specifying amount, type, category, and **handling strict native Dates** (enforced via Pydantic validation & SQLAlchemy Date objects).
3. **Role-Based Access Control (RBAC)**:
   - **Viewer**: Only able to read basic records.
   - **Analyst**: Gets viewer powers PLUS the ability to view the aggregated dashboard summaries.
   - **Admin**: Has immediate, full access across the system (including modifying records and managing users).
4. **Dashboard Summaries**: Using SQL aggregation (`func.sum`), the API automatically calculates the project's total income, total expense, net balance, and totals organized dynamically by category.

## How to Run the Application Locally

1. **Install python packages**:
   Open a terminal in the folder where this code is saved, and install the required dependencies:
   ```bash
   pip install fastapi "pydantic[email]" sqlalchemy uvicorn
   ```

2. **Start the FastAPI server**:
   Use Uvicorn (an ASGI web server) to start the application:
   ```bash
   uvicorn main:app --reload
   ```

3. **View the Automated UI**:
   FastAPI automatically builds an interactive web interface (Swagger) to test our API endpoints natively! Opening the server starts building it.
   Go to your web browser and visit `http://127.0.0.1:8000/docs`.

## 🧪 How to Test and Use the API

In the Swagger UI tool (`http://127.0.0.1:8000/docs`), you can click the **"Try it out"** button on any endpoint to test it directly.

**Authentication Example (Role-Based Checks):**
Instead of a very complex token system (like JWTs) which can be confusing at graduation, authentication is handled neatly by an HTTP Header validation.

To test protected routes (like adding a core asset or reading a dashboard), you must type a valid user email into the `X-User-Email` header text box.

> **Example workflow**:
> 1. Use the **POST `/users/`** endpoint to inject a user: `{ "name": "Admin", "email": "admin@example.com", "role": "admin" }`
> 2. Open the **GET `/dashboard/summary`** endpoint.
> 3. Provide `admin@example.com` into the `x-user-email` parameter window and click **Execute**. It will authenticate and succeed!
> 4. If you create a `viewer` user role exactly the same way, but try to use their email on the dashboard system, it actively shuts the request down with a **403 Forbidden** error.

---
*Created as a comprehensive backend learning assignment!*
