# file: src/models/fact_vehicle_usage.py

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class FactVehicleUsage(Base):
    __tablename__ = 'fact_vehicle_usage'

    usage_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('dim_vehicle.vehicle_id'))
    driver_id = Column(Integer, ForeignKey('dim_driver.driver_id'))
    route_id = Column(Integer, ForeignKey('dim_route.route_id'))
    date_id = Column(Integer, ForeignKey('dim_date.date_id'))
    fuel_id = Column(Integer, ForeignKey('dim_fuel.fuel_id'))
    distance_km = Column(Float)
    fuel_consumption = Column(Float)
    maintenance_cost = Column(Float)

    vehicle = relationship("DimVehicle", back_populates="vehicle_usages")
    driver = relationship("DimDriver", back_populates="vehicle_usages")
    route = relationship("DimRoute", back_populates="vehicle_usages")
    date = relationship("DimDate", back_populates="vehicle_usages")
    fuel = relationship("DimFuel", back_populates = "vehicle_usages")