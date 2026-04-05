from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

import crud
import schemas
import models
from dependencies import get_db, require_viewer, require_admin

router = APIRouter(prefix="/records", tags=["Records"])

@router.post("/", response_model=schemas.RecordResponse, status_code=201, summary="Create a financial record", description="Adds a new financial transaction (income or expense) to the database. Restricted to Admin users.")
def create_record(
    record: schemas.RecordCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(require_admin) # Admin only function
):
    if record.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be either 'income' or 'expense'")
    return crud.create_record(db=db, record=record)

@router.get("/", response_model=List[schemas.RecordResponse], summary="List all records", description="Retrieves financial records with optional filtering by type, category, and precise date boundaries.")
def get_all_records(
    skip: int = 0, 
    limit: int = 100, 
    type: Optional[str] = None, 
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer) # Viewer (or higher) allowed to read
):
    return crud.get_records(
        db, skip=skip, limit=limit, record_type=type, category=category,
        start_date=start_date, end_date=end_date
    )

@router.get("/{record_id}", response_model=schemas.RecordResponse, summary="Get a specific record", description="Fetches a single financial record explicitly by its unique ID. Returns 404 if not found.")
def get_single_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer)
):
    db_record = crud.get_record(db, record_id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.put("/{record_id}", response_model=schemas.RecordResponse, summary="Update a record", description="Modifies the internal details of an existing financial record. Restricted to Admin users.")
def update_record(
    record_id: int, 
    record: schemas.RecordCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin) # Admin only
):
    if record.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be either 'income' or 'expense'")
        
    db_record = crud.update_record(db=db, record_id=record_id, record=record)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.delete("/{record_id}", summary="Delete a record", description="Removes a specific financial record completely from the database. Restricted to Admin users.")
def delete_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin) # Admin only
):
    db_record = crud.delete_record(db=db, record_id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}
