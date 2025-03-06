# file: src/models/fact_warehouse_activity.py

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class FactWarehouseActivity(Base):
    __tablename__ = 'fact_warehouse_activity'

    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('dim_product.product_id'))
    warehouse_id = Column(Integer, ForeignKey('dim_warehouse.warehouse_id'))
    date_id = Column(Integer, ForeignKey('dim_date.date_id'))
    stock_in = Column(Float)
    stock_out = Column(Float)
    storage_time = Column(Float)

    product = relationship("DimProduct", back_populates="warehouse_activities")
    warehouse = relationship("DimWarehouse", back_populates="warehouse_activities")
    date = relationship("DimDate", back_populates="warehouse_activities")