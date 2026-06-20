from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password
from app.api.deps import get_admin_user

router = APIRouter(prefix="/api/employees", tags=["Employee Management"])

@router.get("/")
def get_employees(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    return db.query(User).filter(User.role == "staff").all()

@router.post("/")
def add_employee(full_name: str, email: str, phone: str, password: str,
                  db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    employee = User(
        full_name=full_name,
        email=email,
        phone=phone,
        hashed_password=hash_password(password),
        role="staff",
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.put("/{employee_id}")
def update_employee(employee_id: int, full_name: str = None, phone: str = None,
                     is_active: bool = None,
                     db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    employee = db.query(User).filter(User.id == employee_id, User.role == "staff").first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if full_name:
        employee.full_name = full_name
    if phone:
        employee.phone = phone
    if is_active is not None:
        employee.is_active = is_active
    db.commit()
    db.refresh(employee)
    return employee