from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.route import Route
from app.api.deps import get_admin_user, get_staff_or_admin_user

router = APIRouter(prefix="/api/routes", tags=["Route Management"])

@router.get("/")
def get_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()

@router.post("/")
def add_route(origin: str, destination: str, distance_km: float, base_fare: float,
              db: Session = Depends(get_db), staff=Depends(get_staff_or_admin_user)):
    route = Route(origin=origin, destination=destination, distance_km=distance_km, base_fare=base_fare)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

@router.put("/{route_id}")
def update_route(route_id: int, origin: str = None, destination: str = None, distance_km: float = None, base_fare: float = None,
                  db: Session = Depends(get_db), staff=Depends(get_staff_or_admin_user)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if origin: route.origin = origin
    if destination: route.destination = destination
    if distance_km: route.distance_km = distance_km
    if base_fare: route.base_fare = base_fare
    db.commit()
    db.refresh(route)
    return route

@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    db.delete(route)
    db.commit()
    return {"message": "Route deleted successfully"}