# file: src/etl/load_data.py

from faker.proxy import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.config import DATABASE_URL
from src.etl.generate_data import generate_dim_data, generate_fact_data, truncate_string
from src.models import *
import random


# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind = engine)
session = Session()
fake = Faker('pl_PL')

def load_data() :
    # Generate dimension data
    dim_data = generate_dim_data()

    # Load dimension data
    for customer in dim_data["customers"] :
        session.add(customer)
    for route in dim_data["routes"] :
        session.add(route)
    for vehicle in dim_data["vehicles"] :
        session.add(vehicle)
    for driver in dim_data["drivers"] :
        session.add(driver)
    for warehouse in dim_data["warehouses"] :
        session.add(warehouse)
    for product in dim_data["products"] :
        session.add(product)
    for date in dim_data["dates"] :
        session.add(date)
    for fuel in dim_data["fuels"] :
        session.add(fuel)

    session.commit()  # Commit dimension data to ensure IDs are generated

    # Generate fact data
    fact_data = generate_fact_data(dim_data)

    # Load shipments first
    shipments = fact_data["shipments"]
    for shipment in shipments :
        session.add(shipment)
    session.commit()  # Commit shipments to ensure shipment_id is generated


    # Load remaining fact data
    for usage in fact_data["vehicle_usages"] :
        session.add(usage)
    for activity in fact_data["warehouse_activities"] :
        session.add(activity)

    session.commit()


if __name__ == "__main__" :
    load_data()
    print("Data loaded successfully!")