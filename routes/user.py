from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from dependencies import get_db, require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse, status_code=201, summary="Create a new user", description="Registers a new user in the system. Fails with a 400 error if the email is already registered.")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), admin_user = Depends(require_admin)):
    # Check if user with same email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")
        
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserResponse], summary="List all users", description="Retrieves a list of all registered users. Access is restricted to Admin users entirely.")
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin) # Only admin can view the list of all users
):
    return crud.get_users(db, skip=skip, limit=limit)
