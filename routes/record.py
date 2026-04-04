from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import schemas
import models
from dependencies import get_db, require_viewer, require_admin

router = APIRouter(prefix="/records", tags=["Records"])

@router.post("/", response_model=schemas.RecordResponse, status_code=201)
def create_record(
    record: schemas.RecordCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(require_admin) # Admin only function
):
    if record.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be either 'income' or 'expense'")
    return crud.create_record(db=db, record=record)

@router.get("/", response_model=List[schemas.RecordResponse])
def get_all_records(
    skip: int = 0, 
    limit: int = 100, 
    type: Optional[str] = None, 
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer) # Viewer (or higher) allowed to read
):
    return crud.get_records(db, skip=skip, limit=limit, record_type=type, category=category)

@router.put("/{record_id}", response_model=schemas.RecordResponse)
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

@router.delete("/{record_id}")
def delete_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin) # Admin only
):
    db_record = crud.delete_record(db=db, record_id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}
