# file: src/models/dim_incident.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class DimIncident(Base):
    __tablename__ = 'dim_incident'

    incident_id = Column(Integer, primary_key=True, autoincrement=True)
    shipment_id = Column(Integer, ForeignKey('fact_shipments.shipment_id'))
    vehicle_id = Column(Integer, ForeignKey('dim_vehicle.vehicle_id'))
    date_id = Column(Integer, ForeignKey('dim_date.date_id'))
    incident_type = Column(String(50))
    description = Column(String(200))
    cost_impact = Column(Float)