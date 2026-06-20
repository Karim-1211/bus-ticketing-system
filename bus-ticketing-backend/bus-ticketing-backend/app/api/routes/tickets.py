from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, require_admin
from app.db.session import get_db

router = APIRouter()

@router.get("/")
def list_items(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return []

@router.post("/", status_code=201)
def create_item(db: Session = Depends(get_db), _=Depends(require_admin)):
    return {}

@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return {}

@router.put("/{item_id}")
def update_item(item_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    return {}

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    return None
