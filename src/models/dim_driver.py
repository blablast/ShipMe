# file: src/models/dim_driver.py

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from .base import Base

class DimDriver(Base):
    __tablename__ = 'dim_driver'

    driver_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    license_number = Column(String(20))
    experience_years = Column(Float)
    hire_date = Column(Date)

    shipments = relationship("FactShipments", back_populates="driver")
    vehicle_usages = relationship("FactVehicleUsage", back_populates="driver")