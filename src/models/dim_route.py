# file: src/models/dim_route.py

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class DimRoute(Base):
    __tablename__ = 'dim_route'

    route_id = Column(Integer, primary_key=True, autoincrement=True)
    start_location = Column(String(50))
    start_latitude = Column(Float)
    start_longitude = Column(Float)
    end_location = Column(String(50))
    end_latitude = Column(Float)
    end_longitude = Column(Float)
    distance_km = Column(Float)
    estimated_time_hours = Column(Float)
    road_type = Column(String(20))

    shipments = relationship("FactShipments", back_populates="route")
    vehicle_usages = relationship("FactVehicleUsage", back_populates="route")