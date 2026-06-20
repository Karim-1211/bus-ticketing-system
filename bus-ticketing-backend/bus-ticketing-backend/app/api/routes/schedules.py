from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.models.schedule import Schedule
from app.models.seat import Seat
from app.models.bus import Bus
from app.api.deps import get_admin_user, get_staff_or_admin_user

router = APIRouter(prefix="/api/schedules", tags=["Schedule Management"])

@router.get("/")
def get_schedules(db: Session = Depends(get_db)):
    return db.query(Schedule).all()

@router.post("/")
def add_schedule(bus_id: int, route_id: int, departure_time: datetime, arrival_time: datetime,
                  db: Session = Depends(get_db), staff=Depends(get_staff_or_admin_user)):
    schedule = Schedule(bus_id=bus_id, route_id=route_id, departure_time=departure_time, arrival_time=arrival_time)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    for i in range(1, bus.total_seats + 1):
        seat = Seat(schedule_id=schedule.id, seat_number=str(i))
        db.add(seat)
    db.commit()
    return {"message": "Schedule created with seats", "schedule_id": schedule.id}

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted"}