# file: src/models/dim_driver.py

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from .base import Base

class DimVehicle(Base):
    __tablename__ = 'dim_vehicle'

    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    registration_number = Column(String(20))
    vehicle_type = Column(String(20))
    capacity_kg = Column(Float)
    fuel_type = Column(String(20))
    purchase_date = Column(Date)

    shipments = relationship("FactShipments", back_populates="vehicle")
    vehicle_usages = relationship("FactVehicleUsage", back_populates="vehicle")