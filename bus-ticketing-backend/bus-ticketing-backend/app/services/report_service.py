"""Report aggregation helpers."""
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.payment import Payment

def daily_totals(db: Session, report_date: date) -> dict:
    result = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.paid_at) == report_date,
        Payment.status == "completed",
    ).scalar()
    return {"date": str(report_date), "total": result or 0}
