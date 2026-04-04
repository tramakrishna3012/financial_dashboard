from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas
from dependencies import get_db, require_analyst

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db), 
    user: models.User = Depends(require_analyst) # restricted to Analyst or Admin
):
    # Total Income
    total_income = db.query(func.sum(models.Record.amount)) \
        .filter(models.Record.type == "income").scalar() or 0.0
    
    # Total Expense
    total_expense = db.query(func.sum(models.Record.amount)) \
        .filter(models.Record.type == "expense").scalar() or 0.0
    
    # Net Balance (Calculated value)
    net_balance = total_income - total_expense
    
    # Category-wise totals grouping
    category_grouped = db.query(
        models.Record.category, 
        func.sum(models.Record.amount)
    ).group_by(models.Record.category).all()
    
    # Convert query returns list of tuples into a convenient dictionary
    category_totals = {category: amount for category, amount in category_grouped}
    
    return schemas.DashboardSummary(
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        category_totals=category_totals
    )
