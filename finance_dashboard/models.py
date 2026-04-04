from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="viewer") # expected roles: viewer, analyst, admin
    is_active = Column(Boolean, default=True)

    # Establish a relationship with the Record model
    records = relationship("Record", back_populates="owner")

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    type = Column(String) # "income" or "expense"
    category = Column(String) # e.g., "Salary", "Food", "Rent"
    
    # We use Date type instead of String because it enforces proper date formats at the database level,
    # allows for chronological sorting, and prevents invalid data entry (e.g., "random text" instead of a date).
    date = Column(Date) 
    
    notes = Column(String, nullable=True)

    # Establish a relationship back to the User model
    owner = relationship("User", back_populates="records")
