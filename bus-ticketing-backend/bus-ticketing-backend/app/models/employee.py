from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employee_code = Column(String, unique=True, nullable=False)
    designation = Column(String, nullable=False)  # counter_staff, manager
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")