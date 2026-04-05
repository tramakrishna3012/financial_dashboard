from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import defaultdict

import crud
import models
import schemas
from dependencies import get_db, require_analyst

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=schemas.DashboardSummary, summary="Get dashboard totals", description="Calculates the overall project total income, total expenses, net balance, and seamlessly aggregates sums natively by category.")
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

@router.get("/recent", response_model=list[schemas.RecordResponse], summary="Get recent activity", description="Fetches the most recently added financial records strictly ordered by their action date descending.")
def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_analyst)
):
    return crud.get_recent_records(db, limit=limit)

@router.get("/trends", summary="Get monthly trends", description="Deeply groups financial records by Year/Month keys and maps income vs expenses out dynamically.")
def get_monthly_trends(
    db: Session = Depends(get_db),
    user: models.User = Depends(require_analyst)
):
    records = db.query(models.Record).all()
    monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for r in records:
        key = f"{r.date.year}-{str(r.date.month).zfill(2)}"
        monthly[key][r.type] += r.amount
    return {"monthly_trends": dict(sorted(monthly.items()))}
