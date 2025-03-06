# file: src/models/dim_date.py

from sqlalchemy import Column, Integer, Date, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class DimDate(Base):
    __tablename__ = 'dim_date'

    date_id = Column(Integer, primary_key=True, autoincrement=True)
    full_date = Column(Date)
    day = Column(Integer)
    month = Column(Integer)
    quarter = Column(Integer)
    year = Column(Integer)
    is_holiday = Column(Boolean)

    shipments = relationship("FactShipments", back_populates="date")
    vehicle_usages = relationship("FactVehicleUsage", back_populates="date")
    warehouse_activities = relationship("FactWarehouseActivity", back_populates="date")