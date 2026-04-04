from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from dependencies import get_db, require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user with same email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")
    
    # Ensure role is valid
    if user.role not in ["viewer", "analyst", "admin"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid role. Must be 'viewer', 'analyst', or 'admin'."
        )
        
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin) # Only admin can view the list of all users
):
    return crud.get_users(db, skip=skip, limit=limit)
