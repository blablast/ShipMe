"""Add indexes for performance optimization

Revision ID: 149ea8aa79ba
Revises: f6ff4d0c40be
Create Date: 2025-03-06 12:07:44.258716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '149ea8aa79ba'
down_revision: Union[str, None] = 'f6ff4d0c40be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Indeksy dla fact_shipments
    op.create_index('idx_fact_shipments_customer_id', 'fact_shipments', ['customer_id'], unique=False)
    op.create_index('idx_fact_shipments_route_id', 'fact_shipments', ['route_id'], unique=False)
    op.create_index('idx_fact_shipments_driver_id', 'fact_shipments', ['driver_id'], unique=False)
    op.create_index('idx_fact_shipments_date_id', 'fact_shipments', ['date_id'], unique=False)
    op.create_index('idx_fact_shipments_warehouse_id', 'fact_shipments', ['warehouse_id'], unique=False)
    op.create_index('idx_fact_shipments_vehicle_id', 'fact_shipments', ['vehicle_id'], unique=False)
    op.create_index('idx_fact_shipments_shipping_cost', 'fact_shipments', ['shipping_cost'], unique=False)

    # Indeksy dla dim_incident
    op.create_index('idx_dim_incident_shipment_id', 'dim_incident', ['shipment_id'], unique=False)
    op.create_index('idx_dim_incident_date_id', 'dim_incident', ['date_id'], unique=False)
    op.create_index('idx_dim_incident_incident_type', 'dim_incident', ['incident_type'], unique=False)

    # Indeksy dla fact_vehicle_usage
    op.create_index('idx_fact_vehicle_usage_vehicle_id', 'fact_vehicle_usage', ['vehicle_id'], unique=False)
    op.create_index('idx_fact_vehicle_usage_route_id', 'fact_vehicle_usage', ['route_id'], unique=False)
    op.create_index('idx_fact_vehicle_usage_fuel_id', 'fact_vehicle_usage', ['fuel_id'], unique=False)
    op.create_index('idx_fact_vehicle_usage_date_id', 'fact_vehicle_usage', ['date_id'], unique=False)

    # Indeksy dla fact_warehouse_activity
    op.create_index('idx_fact_warehouse_activity_warehouse_id', 'fact_warehouse_activity', ['warehouse_id'], unique=False)
    op.create_index('idx_fact_warehouse_activity_product_id', 'fact_warehouse_activity', ['product_id'], unique=False)

    # Opcjonalne indeksy dla tabel wymiarów
    op.create_index('idx_dim_date_month_year', 'dim_date', ['month', 'year'], unique=False)
    op.create_index('idx_dim_date_full_date', 'dim_date', ['full_date'], unique=False)
    op.create_index('idx_dim_vehicle_vehicle_type', 'dim_vehicle', ['vehicle_type'], unique=False)
    op.create_index('idx_dim_route_road_type', 'dim_route', ['road_type'], unique=False)

def downgrade():
    # Usuwanie indeksów w odwrotnej kolejności
    op.drop_index('idx_dim_route_road_type', table_name='dim_route')
    op.drop_index('idx_dim_vehicle_vehicle_type', table_name='dim_vehicle')
    op.drop_index('idx_dim_date_full_date', table_name='dim_date')
    op.drop_index('idx_dim_date_month_year', table_name='dim_date')
    op.drop_index('idx_fact_warehouse_activity_product_id', table_name='fact_warehouse_activity')
    op.drop_index('idx_fact_warehouse_activity_warehouse_id', table_name='fact_warehouse_activity')
    op.drop_index('idx_fact_vehicle_usage_date_id', table_name='fact_vehicle_usage')
    op.drop_index('idx_fact_vehicle_usage_fuel_id', table_name='fact_vehicle_usage')
    op.drop_index('idx_fact_vehicle_usage_route_id', table_name='fact_vehicle_usage')
    op.drop_index('idx_fact_vehicle_usage_vehicle_id', table_name='fact_vehicle_usage')
    op.drop_index('idx_dim_incident_incident_type', table_name='dim_incident')
    op.drop_index('idx_dim_incident_date_id', table_name='dim_incident')
    op.drop_index('idx_dim_incident_shipment_id', table_name='dim_incident')
    op.drop_index('idx_fact_shipments_shipping_cost', table_name='fact_shipments')
    op.drop_index('idx_fact_shipments_vehicle_id', table_name='fact_shipments')
    op.drop_index('idx_fact_shipments_warehouse_id', table_name='fact_shipments')
    op.drop_index('idx_fact_shipments_date_id', table_name='fact_shipments')
    op.drop_index('idx_fact_shipments_driver_id', table_name='fact_shipments')
    op.drop_index('idx_fact_shipments_route_id', table_name='fact_shipments')
    op.drop_index('idx_fact_shipments_customer_id', table_name='fact_shipments')