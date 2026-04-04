from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# Provides a database session and safely closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock Authentication using Header (Simple approach instead of complete Auth flow)
# The user's role is determined by the email given in the 'X-User-Email' header
def get_current_user(x_user_email: str = Header(None), db: Session = Depends(get_db)):
    if not x_user_email:
        raise HTTPException(
            status_code=401, 
            detail="Missing 'X-User-Email' header. Please authenticate."
        )
    
    user = db.query(models.User).filter(models.User.email == x_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in system.")
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is inactive.")
        
    return user

# Role-based dependency: Any authenticated user (viewer, analyst, admin)
def require_viewer(current_user: models.User = Depends(get_current_user)):
    return current_user

# Role-based dependency: Analyst or Admin
def require_analyst(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(
            status_code=403, 
            detail="Access forbidden. Requires 'analyst' or 'admin' role."
        )
    return current_user

# Role-based dependency: Admin only
def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Access forbidden. Requires 'admin' role."
        )
    return current_user
