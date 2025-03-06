# file: src/models/dim_customer.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class DimCustomer(Base):
    __tablename__ = 'dim_customer'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address = Column(String(100))
    city = Column(String(50))
    country = Column(String(50))
    customer_type = Column(String(20))

    shipments = relationship("FactShipments", back_populates="customer")