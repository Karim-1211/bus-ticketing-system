from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.base import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    distance_km = Column(Float, nullable=True)
    base_fare = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)