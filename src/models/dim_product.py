# file: src/models/dim_product.py

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class DimProduct(Base):
    __tablename__ = 'dim_product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(50))
    category = Column(String(50))
    weight_kg = Column(Float)
    fragility = Column(String(20))

    warehouse_activities = relationship("FactWarehouseActivity", back_populates="product")