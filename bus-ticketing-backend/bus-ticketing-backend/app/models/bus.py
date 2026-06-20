from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, nullable=False)
    bus_name = Column(String, nullable=False)
    bus_type = Column(String, nullable=False)  # AC, Non-AC
    total_seats = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)