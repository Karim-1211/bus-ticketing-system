from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NULL = walk-in customer, no account
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    passenger_name = Column(String, nullable=True)
    passenger_phone = Column(String, nullable=True)
    booked_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # which staff member created it (NULL = self-booked)
    status = Column(String, default="confirmed")  # confirmed, cancelled
    booked_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", foreign_keys=[user_id])
    booked_by = relationship("User", foreign_keys=[booked_by_id])
    schedule = relationship("Schedule")
    seat = relationship("Seat")