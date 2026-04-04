from sqlalchemy.orm import Session
import models
import schemas

# ================= USER CRUD =================

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ================ RECORD CRUD ================

def get_record(db: Session, record_id: int):
    return db.query(models.Record).filter(models.Record.id == record_id).first()

def get_records(db: Session, skip: int = 0, limit: int = 100, record_type: str = None, category: str = None):
    query = db.query(models.Record)
    
    # Apply optional filters
    if record_type:
        query = query.filter(models.Record.type == record_type)
    if category:
        query = query.filter(models.Record.category == category)
        
    return query.offset(skip).limit(limit).all()

def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.Record(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_record(db: Session, record_id: int, record: schemas.RecordCreate):
    db_record = get_record(db, record_id)
    if db_record:
        # Update the properties of the record
        for key, value in record.model_dump().items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int):
    db_record = get_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record
