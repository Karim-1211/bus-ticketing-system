from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.bus import Bus
from app.api.deps import get_admin_user, get_staff_or_admin_user

router = APIRouter(prefix="/api/buses", tags=["Bus Management"])

@router.get("/")
def get_buses(db: Session = Depends(get_db)):
    return db.query(Bus).all()

@router.post("/")
def add_bus(bus_number: str, bus_name: str, bus_type: str, total_seats: int, image_url: str = None,
            db: Session = Depends(get_db), staff=Depends(get_staff_or_admin_user)):
    existing = db.query(Bus).filter(Bus.bus_number == bus_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bus number already exists")
    bus = Bus(bus_number=bus_number, bus_name=bus_name, bus_type=bus_type, total_seats=total_seats, image_url=image_url)
    db.add(bus)
    db.commit()
    db.refresh(bus)
    return bus

@router.put("/{bus_id}")
def update_bus(bus_id: int, bus_name: str = None, bus_type: str = None, total_seats: int = None, image_url: str = None,
               db: Session = Depends(get_db), staff=Depends(get_staff_or_admin_user)):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    if bus_name: bus.bus_name = bus_name
    if bus_type: bus.bus_type = bus_type
    if total_seats: bus.total_seats = total_seats
    if image_url: bus.image_url = image_url
    db.commit()
    db.refresh(bus)
    return bus

@router.delete("/{bus_id}")
def delete_bus(bus_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    db.delete(bus)
    db.commit()
    return {"message": "Bus deleted successfully"}