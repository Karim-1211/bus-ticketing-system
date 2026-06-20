"""Seat-locking logic to prevent double-booking."""
from sqlalchemy.orm import Session
from app.models.seat import Seat

def lock_seat(db: Session, seat_id: int) -> bool:
    seat = db.query(Seat).filter(Seat.id == seat_id, Seat.is_available == True).with_for_update().first()
    if not seat:
        return False
    seat.is_available = False
    db.commit()
    return True

def release_seat(db: Session, seat_id: int) -> None:
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if seat:
        seat.is_available = True
        db.commit()
