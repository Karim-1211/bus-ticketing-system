from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.booking import Booking
from app.models.seat import Seat
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.models.schedule import Schedule
from app.models.route import Route
from app.api.deps import get_current_user, get_admin_user, get_staff_or_admin_user
from app.services.notification_service import notify
import uuid

router = APIRouter(prefix="/api/bookings", tags=["Booking"])


@router.get("/seats/{schedule_id}")
def get_seats(schedule_id: int, db: Session = Depends(get_db)):
    return db.query(Seat).filter(Seat.schedule_id == schedule_id).all()


@router.post("/")
def book_ticket(schedule_id: int, seat_id: int, payment_method: str = "online",
                db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if not seat or seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat not available")

    booking = Booking(
        user_id=current_user.id,
        schedule_id=schedule_id,
        seat_id=seat_id,
        passenger_name=current_user.full_name,
        passenger_phone=current_user.phone,
    )
    db.add(booking)
    seat.is_booked = True
    db.commit()
    db.refresh(booking)

    ticket = Ticket(booking_id=booking.id, ticket_number=str(uuid.uuid4())[:8].upper())
    db.add(ticket)

    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    route = db.query(Route).filter(Route.id == schedule.route_id).first()
    payment = Payment(booking_id=booking.id, amount=route.base_fare, payment_method=payment_method)
    db.add(payment)
    db.commit()
    db.refresh(ticket)

    notify(db, current_user.id,
           f"Your booking #{booking.id} is confirmed! Ticket {ticket.ticket_number}, seat {seat.seat_number}.",
           "confirmation")

    return {
        "message": "Booking confirmed",
        "booking_id": booking.id,
        "ticket_number": ticket.ticket_number,
        "passenger_name": booking.passenger_name,
        "seat_number": seat.seat_number,
        "departure_time": schedule.departure_time,
        "arrival_time": schedule.arrival_time,
        "fare": route.base_fare,
        "payment_method": payment_method,
    }


@router.post("/walkin")
def book_ticket_walkin(schedule_id: int, seat_id: int, passenger_name: str, passenger_phone: str,
                        db: Session = Depends(get_db), staff=Depends(get_staff_or_admin_user)):
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if not seat or seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat not available")

    booking = Booking(
        user_id=None,
        schedule_id=schedule_id,
        seat_id=seat_id,
        passenger_name=passenger_name,
        passenger_phone=passenger_phone,
        booked_by_id=staff.id,
    )
    db.add(booking)
    seat.is_booked = True
    db.commit()
    db.refresh(booking)

    ticket = Ticket(booking_id=booking.id, ticket_number=str(uuid.uuid4())[:8].upper())
    db.add(ticket)

    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    route = db.query(Route).filter(Route.id == schedule.route_id).first()
    payment = Payment(booking_id=booking.id, amount=route.base_fare, payment_method="cash")
    db.add(payment)
    db.commit()

    return {"message": "Walk-in booking confirmed", "booking_id": booking.id, "ticket_number": ticket.ticket_number}


@router.get("/history")
def booking_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.id.desc()).all()

    result = []
    for b in bookings:
        ticket = db.query(Ticket).filter(Ticket.booking_id == b.id).first()
        payment = db.query(Payment).filter(Payment.booking_id == b.id).first()
        result.append({
            "id": b.id,
            "schedule_id": b.schedule_id,
            "seat_id": b.seat_id,
            "status": b.status,
            "booked_at": b.booked_at,
            "ticket_number": ticket.ticket_number if ticket else None,
            "payment_method": payment.payment_method if payment else None,
            "payment_status": payment.status if payment else None,
            "amount": payment.amount if payment else None,
        })
    return result


@router.get("/staff-history")
def staff_booking_history(db: Session = Depends(get_db), staff=Depends(get_staff_or_admin_user)):
    return db.query(Booking).filter(Booking.booked_by_id == staff.id).all()


@router.get("/all")
def all_bookings(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(Booking).all()


@router.put("/cancel/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    is_owner = booking.user_id == current_user.id
    is_creator_staff = current_user.role == "staff" and booking.booked_by_id == current_user.id
    is_admin = current_user.role == "admin"

    if not (is_owner or is_creator_staff or is_admin):
        raise HTTPException(status_code=403, detail="You do not have permission to cancel this booking")

    booking.status = "cancelled"
    seat = db.query(Seat).filter(Seat.id == booking.seat_id).first()
    seat.is_booked = False
    ticket = db.query(Ticket).filter(Ticket.booking_id == booking_id).first()
    if ticket:
        ticket.status = "cancelled"
    payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if payment:
        payment.status = "refunded"
    db.commit()

    if booking.user_id:
        notify(db, booking.user_id,
               f"Your booking #{booking.id} has been cancelled. Refund processed.",
               "cancellation")

    return {"message": "Booking cancelled and refunded"}