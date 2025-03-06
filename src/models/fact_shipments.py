# file: src/models/fact_shipments.py

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class FactShipments(Base):
    __tablename__ = 'fact_shipments'

    shipment_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('dim_customer.customer_id'))
    route_id = Column(Integer, ForeignKey('dim_route.route_id'))
    vehicle_id = Column(Integer, ForeignKey('dim_vehicle.vehicle_id'))
    driver_id = Column(Integer, ForeignKey('dim_driver.driver_id'))
    warehouse_id = Column(Integer, ForeignKey('dim_warehouse.warehouse_id'))
    date_id = Column(Integer, ForeignKey('dim_date.date_id'))
    weight = Column(Float)
    shipping_cost = Column(Float)
    delivery_time = Column(Float)

    customer = relationship("DimCustomer", back_populates="shipments")
    route = relationship("DimRoute", back_populates="shipments")
    vehicle = relationship("DimVehicle", back_populates="shipments")
    driver = relationship("DimDriver", back_populates="shipments")
    warehouse = relationship("DimWarehouse", back_populates="shipments")
    date = relationship("DimDate", back_populates="shipments")