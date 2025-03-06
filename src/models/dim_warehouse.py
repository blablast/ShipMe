# file: src/models/dim_warehouse.py

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class DimWarehouse(Base):
    __tablename__ = 'dim_warehouse'

    warehouse_id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_name = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    capacity_m3 = Column(Float)

    shipments = relationship("FactShipments", back_populates="warehouse")
    warehouse_activities = relationship("FactWarehouseActivity", back_populates="warehouse")