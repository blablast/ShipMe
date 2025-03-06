# file: src/models/dim_fuel.py

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from .base import Base

class DimFuel(Base):
    __tablename__ = 'dim_fuel'

    fuel_id = Column(Integer, primary_key=True, autoincrement=True)
    fuel_type = Column(String(20))
    price_per_liter = Column(Float)
    supplier_name = Column(String(50))
    purchase_date = Column(Date)

    vehicle_usages = relationship("FactVehicleUsage", back_populates = "fuel")