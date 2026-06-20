from sqlalchemy.orm import Session
from app.models.notification import Notification


def notify(db: Session, user_id: int, message: str, type: str = "confirmation"):
    if not user_id:
        return None
    note = Notification(user_id=user_id, message=message, type=type)
    db.add(note)
    db.commit()
    return note