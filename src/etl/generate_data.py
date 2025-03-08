# file: src/etl/generate_data.py

from faker import Faker
import random
from datetime import datetime, timedelta
from src.models import (
    DimCustomer, DimRoute, DimVehicle, DimDriver, DimWarehouse, DimProduct, DimDate,
    DimIncident, DimFuel,
    FactShipments, FactVehicleUsage, FactWarehouseActivity
)

fake = Faker('pl_PL')

# Polish cities with their coordinates
POLISH_CITIES = {
    "Warszawa": {"latitude": 52.2297, "longitude": 21.0122},
    "Kraków": {"latitude": 50.0647, "longitude": 19.9450},
    "Gdańsk": {"latitude": 54.3520, "longitude": 18.6466},
    "Wrocław": {"latitude": 51.1079, "longitude": 17.0385},
    "Poznań": {"latitude": 52.4064, "longitude": 16.9252},
    "Łódź": {"latitude": 51.7592, "longitude": 19.4550},
    "Katowice": {"latitude": 50.2649, "longitude": 19.0238},
    "Szczecin": {"latitude": 53.4285, "longitude": 14.5528},
    "Bydgoszcz": {"latitude": 53.1235, "longitude": 18.0084},
    "Lublin": {"latitude": 51.2465, "longitude": 22.5684},
}


def truncate_string(text, max_length):
    """Truncate string to max_length characters"""
    return text[:max_length] if len(text) > max_length else text

def generate_dim_data():
    """
    Generate dimension data for the ETL process
    """
    customers = []
    routes = []
    vehicles = []
    drivers = []
    warehouses = []
    products = []
    dates = []
    incidents = []
    fuels = []

    # Generate 100 customers
    for _ in range(200):
        city = random.choice(list(POLISH_CITIES.keys()))
        customer = DimCustomer(
            first_name=truncate_string(fake.first_name(), 50),
            last_name=truncate_string(fake.last_name(), 50),
            address=truncate_string(fake.street_address(), 100),
            city=city,
            country="Poland",
            customer_type=random.choice(["individual", "business"])
        )
        customers.append(customer)

    # Generate 50 routes
    for _ in range(100):
        start_city = random.choice(list(POLISH_CITIES.keys()))
        end_city = random.choice(list(POLISH_CITIES.keys()))
        while start_city == end_city:  # Ensure start and end are different
            end_city = random.choice(list(POLISH_CITIES.keys()))
        route = DimRoute(
            start_location=start_city,
            start_latitude=POLISH_CITIES[start_city]["latitude"],
            start_longitude=POLISH_CITIES[start_city]["longitude"],
            end_location=end_city,
            end_latitude=POLISH_CITIES[end_city]["latitude"],
            end_longitude=POLISH_CITIES[end_city]["longitude"],
            distance_km=round(random.uniform(50, 1000), 2),
            estimated_time_hours=round(random.uniform(1, 48), 2),
            road_type=random.choice(["highway", "local"])
        )
        routes.append(route)

    # Generate 20 vehicles
    for _ in range(50):
        vehicle = DimVehicle(
            registration_number=truncate_string(fake.license_plate(), 20),
            vehicle_type=random.choice(["truck", "van", "car"]),
            capacity_kg=round(random.uniform(1000, 20000), 2),
            fuel_type=random.choice(["diesel", "petrol", "electric"]),
            purchase_date=fake.date_this_decade()
        )
        vehicles.append(vehicle)

    # Generate 30 drivers
    for _ in range(60):
        driver = DimDriver(
            first_name=truncate_string(fake.first_name(), 50),
            last_name=truncate_string(fake.last_name(), 50),
            license_number=truncate_string(fake.bothify(text="DRV#####"), 20),
            experience_years=round(random.uniform(1, 20), 1),
            hire_date=fake.date_this_decade()
        )
        drivers.append(driver)

    # Generate 10 warehouses
    for _ in range(10):
        city = random.choice(list(POLISH_CITIES.keys()))
        warehouse = DimWarehouse(
            warehouse_name=truncate_string(fake.company(), 50),
            city=city,
            country="Poland",
            latitude=POLISH_CITIES[city]["latitude"],
            longitude=POLISH_CITIES[city]["longitude"],
            capacity_m3=round(random.uniform(1000, 10000), 2)
        )
        warehouses.append(warehouse)

    # Generate 50 products
    for _ in range(200):
        product = DimProduct(
            product_name=truncate_string(fake.word(), 50),
            category=truncate_string(fake.word(), 50),
            weight_kg=round(random.uniform(0.1, 50), 2),
            fragility=random.choice(["fragile", "standard"])
        )
        products.append(product)

    # Generate dates for two years (365 days)
    start_date = datetime(2023, 1, 1)
    for i in range(365*3):
        date = DimDate(
            full_date=start_date + timedelta(days=i),
            day=(start_date + timedelta(days=i)).day,
            month=(start_date + timedelta(days=i)).month,
            quarter=((start_date + timedelta(days=i)).month - 1) // 3 + 1,
            year=(start_date + timedelta(days=i)).year,
            is_holiday=random.choice([True, False])
        )
        dates.append(date)

    # Generate 30 fuels
    for _ in range(30):
        fuel = DimFuel(
            fuel_type=random.choice(["diesel", "petrol", "electric"]),
            price_per_liter=round(random.uniform(1, 10), 2),
            supplier_name=truncate_string(fake.company(), 50),
            purchase_date=fake.date_this_year()
        )
        fuels.append(fuel)

    return {
        "customers": customers,
        "routes": routes,
        "vehicles": vehicles,
        "drivers": drivers,
        "warehouses": warehouses,
        "products": products,
        "dates": dates,
        "fuels": fuels,
        "incidents": incidents
    }

def generate_fact_data(dim_data):
    shipments = []
    vehicle_usages = []
    warehouse_activities = []
    incidents = []

    for _ in range(2000):
        shipment = FactShipments(
            customer_id=random.choice(dim_data["customers"]).customer_id,
            route_id=random.choice(dim_data["routes"]).route_id,
            vehicle_id=random.choice(dim_data["vehicles"]).vehicle_id,
            driver_id=random.choice(dim_data["drivers"]).driver_id,
            warehouse_id=random.choice(dim_data["warehouses"]).warehouse_id,
            date_id=random.choice(dim_data["dates"]).date_id,
            weight=round(random.uniform(1, 100), 2),
            shipping_cost=round(random.uniform(10, 500), 2),
            delivery_time=round(random.uniform(1, 72), 2)
        )
        shipments.append(shipment)

    for _ in range(200):
        incident = DimIncident(
            shipment_id=random.choice(shipments).shipment_id,
            vehicle_id=random.choice(dim_data["vehicles"]).vehicle_id,
            date_id=random.choice(dim_data["dates"]).date_id,
            incident_type=truncate_string(random.choice(["accident", "delay", "damage"]), 50),
            description=truncate_string(fake.sentence(), 200),
            cost_impact=round(random.uniform(50, 1000), 2)
        )
        incidents.append(incident)

    for _ in range(1500):
        usage = FactVehicleUsage(
            vehicle_id=random.choice(dim_data["vehicles"]).vehicle_id,
            driver_id=random.choice(dim_data["drivers"]).driver_id,
            route_id=random.choice(dim_data["routes"]).route_id,
            date_id=random.choice(dim_data["dates"]).date_id,
            fuel_id=random.choice(dim_data["fuels"]).fuel_id,
            distance_km=round(random.uniform(10, 500), 2),
            fuel_consumption=round(random.uniform(5, 50), 2),
            maintenance_cost=round(random.uniform(0, 200), 2)
        )
        vehicle_usages.append(usage)

    for _ in range(2000):
        activity = FactWarehouseActivity(
            product_id=random.choice(dim_data["products"]).product_id,
            warehouse_id=random.choice(dim_data["warehouses"]).warehouse_id,
            date_id=random.choice(dim_data["dates"]).date_id,
            stock_in=round(random.uniform(0, 100), 2),
            stock_out=round(random.uniform(0, 100), 2),
            storage_time=round(random.uniform(1, 30), 2)
        )
        warehouse_activities.append(activity)

    return {
        "shipments": shipments,
        "vehicle_usages": vehicle_usages,
        "warehouse_activities": warehouse_activities,
        "incidents": incidents
    }

if __name__ == "__main__":
    dim_data = generate_dim_data()
    fact_data = generate_fact_data(dim_data)
    print("Generated dimension data:", {key: len(value) for key, value in dim_data.items()})
    print("Generated fact data:", {key: len(value) for key, value in fact_data.items()})