from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from app.db.session import get_db
from app.models.booking import Booking
from app.models.payment import Payment
from app.api.deps import get_admin_user, get_staff_or_admin_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/daily")
def daily_report(report_date: date = None, db: Session = Depends(get_db),
                  staff=Depends(get_staff_or_admin_user)):
    if not report_date:
        report_date = date.today()
    bookings = db.query(Booking).filter(func.date(Booking.booked_at) == report_date).all()
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.paid_at) == report_date
    ).scalar() or 0
    return {"date": str(report_date), "total_bookings": len(bookings), "total_revenue": total_revenue}


@router.get("/weekly")
def weekly_report(report_date: date = None, db: Session = Depends(get_db),
                   admin=Depends(get_admin_user)):
    if not report_date:
        report_date = date.today()
    start_of_week = report_date - timedelta(days=report_date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)                      # Sunday

    bookings = db.query(Booking).filter(
        func.date(Booking.booked_at) >= start_of_week,
        func.date(Booking.booked_at) <= end_of_week
    ).all()
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.paid_at) >= start_of_week,
        func.date(Payment.paid_at) <= end_of_week
    ).scalar() or 0
    return {
        "week_start": str(start_of_week),
        "week_end": str(end_of_week),
        "total_bookings": len(bookings),
        "total_revenue": total_revenue
    }


@router.get("/monthly")
def monthly_report(year: int, month: int, db: Session = Depends(get_db),
                    admin=Depends(get_admin_user)):
    bookings = db.query(Booking).filter(
        func.extract('year', Booking.booked_at) == year,
        func.extract('month', Booking.booked_at) == month
    ).all()
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        func.extract('year', Payment.paid_at) == year,
        func.extract('month', Payment.paid_at) == month
    ).scalar() or 0
    return {"year": year, "month": month, "total_bookings": len(bookings), "total_revenue": total_revenue}