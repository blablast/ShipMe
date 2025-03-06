# file: src/analysis/queries.py

from sqlalchemy import create_engine, text
import pandas as pd
from src.config import DATABASE_URL

class LogisticsQueries:
    def __init__(self):
        """Initialize the LogisticsQueries class with a database engine."""
        self.engine = create_engine(DATABASE_URL)

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return the result as a pandas DataFrame.
        Automatically names columns based on the query result.
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns= list(result.keys()))
        return df

    def avg_delivery_time_by_city(self, top: int = 5) -> (pd.DataFrame, str):
        query = f"""
        SELECT
            dc.city,
            AVG(fs.delivery_time) as avg_delivery_time,
            COUNT(fs.shipment_id) as shipment_count
        FROM dim_customer dc
        JOIN fact_shipments fs ON dc.customer_id = fs.customer_id
        GROUP BY dc.city
        ORDER BY avg_delivery_time DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

    def most_frequent_drivers(self, top: int = 5) -> (pd.DataFrame, str):
        query = f"""
        SELECT
            dd.first_name,
            dd.last_name,
            COUNT(fs.shipment_id) as shipment_count
        FROM dim_driver dd
        JOIN fact_shipments fs ON dd.driver_id = fs.driver_id
        GROUP BY dd.driver_id, dd.first_name, dd.last_name
        ORDER BY shipment_count DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

    def fuel_costs_per_vehicle_usage(self, top: int = 5) -> (pd.DataFrame, str):
        query = f"""
        SELECT 
            fvu.usage_id,
            dv.vehicle_type,
            df.fuel_type,
            df.price_per_liter,
            fvu.fuel_consumption,
            (df.price_per_liter * fvu.fuel_consumption) as total_fuel_cost
        FROM fact_vehicle_usage fvu
        JOIN dim_vehicle dv ON fvu.vehicle_id = dv.vehicle_id
        JOIN dim_fuel df ON fvu.fuel_id = df.fuel_id
        ORDER BY total_fuel_cost DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

    def total_weight_per_warehouse(self, top: int = 5) -> (pd.DataFrame, str):
        query = f"""
        SELECT 
            dw.warehouse_name, 
            SUM(fs.weight) as total_weight
        FROM dim_warehouse dw
        JOIN fact_shipments fs ON dw.warehouse_id = fs.warehouse_id
        GROUP BY dw.warehouse_id, dw.warehouse_name
        ORDER BY total_weight DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

    def most_expensive_shipments(self, top: int = 5) -> (pd.DataFrame, str):
        query = f"""
        SELECT
            fs.shipment_id,
            dr.start_location,
            dr.end_location,
            dv.vehicle_type,
            fs.shipping_cost,
            fs.weight,
            fs.delivery_time
        FROM fact_shipments fs
        JOIN dim_route dr ON fs.route_id = dr.route_id
        JOIN dim_vehicle dv ON fs.vehicle_id = dv.vehicle_id
        ORDER BY fs.shipping_cost DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

    def incidents_by_type(self, top: int = 5) -> (pd.DataFrame, str):
        query = f"""
        SELECT
            di.incident_type,
            COUNT(di.incident_id) as incident_count,
            SUM(di.cost_impact) as total_cost_impact
        FROM dim_incident di
        GROUP BY di.incident_type
        ORDER BY total_cost_impact DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

    def delivery_time_trends_by_month(self) -> (pd.DataFrame, str):
        query = """
        SELECT
            dd.month,
            dd.year,
            AVG(fs.delivery_time) as avg_delivery_time,
            COUNT(fs.shipment_id) as shipment_count
        FROM dim_date dd
        JOIN fact_shipments fs ON dd.date_id = fs.date_id
        GROUP BY dd.month, dd.year
        ORDER BY dd.year, dd.month;
        """
        return self.execute_query(query), query

    def driver_ranking_by_delivery_time(self, top: int = 5) -> (pd.DataFrame, str):
        query = f"""
        SELECT
            dd.first_name,
            dd.last_name,
            AVG(fs.delivery_time) as avg_delivery_time,
            RANK() OVER (ORDER BY AVG(fs.delivery_time) DESC) as driver_rank
        FROM dim_driver dd
        JOIN fact_shipments fs ON dd.driver_id = fs.driver_id
        GROUP BY dd.driver_id, dd.first_name, dd.last_name
        HAVING COUNT(fs.shipment_id) > 3
        ORDER BY driver_rank
        LIMIT {top};
        """
        return self.execute_query(query), query

    def monthly_delivery_time_changes(self) -> (pd.DataFrame, str):
        query = """
        WITH monthly_avg AS (
            SELECT
                dd.month,
                dd.year,
                AVG(fs.delivery_time) as avg_delivery_time
            FROM dim_date dd
            JOIN fact_shipments fs ON dd.date_id = fs.date_id
            GROUP BY dd.month, dd.year
        )
        SELECT
            month,
            year,
            avg_delivery_time,
            LAG(avg_delivery_time) OVER (ORDER BY year, month) as previous_month_delivery_time,
            (avg_delivery_time - LAG(avg_delivery_time) OVER (ORDER BY year, month)) as time_diff
        FROM monthly_avg
        ORDER BY year, month;
        """
        return self.execute_query(query), query

    def incidents_distribution_over_time(self) -> (pd.DataFrame, str):
        query = """
        WITH date_series AS (
            SELECT
                generate_series(
                    (SELECT MIN(dd.full_date) FROM dim_date dd),
                    (SELECT MAX(dd.full_date) FROM dim_date dd),
                    interval '1 month'
                ) as incident_date
        ),
        incident_counts AS (
            SELECT
                EXTRACT(MONTH FROM dd.full_date) as incident_month,
                EXTRACT(YEAR FROM dd.full_date) as incident_year,
                COUNT(di.incident_id) as incident_count
            FROM dim_incident di
            JOIN dim_date dd ON di.date_id = dd.date_id
            GROUP BY EXTRACT(MONTH FROM dd.full_date), EXTRACT(YEAR FROM dd.full_date)
        )
        SELECT
            EXTRACT(MONTH FROM ds.incident_date) as incident_month,
            EXTRACT(YEAR FROM ds.incident_date) as incident_year,
            COALESCE(ic.incident_count, 0) as incident_count
        FROM date_series ds
        LEFT JOIN incident_counts ic
            ON EXTRACT(MONTH FROM ds.incident_date) = ic.incident_month
            AND EXTRACT(YEAR FROM ds.incident_date) = ic.incident_year
        ORDER BY incident_year, incident_month;
        """
        return self.execute_query(query), query

    def delivery_time_percentiles_by_vehicle_type(self) -> (pd.DataFrame, str):
        """
        Calculate delivery time percentiles (median, 90th percentile) by vehicle type using PostgreSQL's PERCENTILE_CONT.
        Returns a DataFrame with columns: vehicle_type, median_delivery_time, percentile_90_delivery_time.
        """
        query = """
        SELECT
            dv.vehicle_type,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fs.delivery_time) as median_delivery_time,
            PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY fs.delivery_time) as percentile_90_delivery_time
        FROM dim_vehicle dv
        JOIN fact_shipments fs ON dv.vehicle_id = fs.vehicle_id
        GROUP BY dv.vehicle_type
        ORDER BY median_delivery_time DESC;
        """
        return self.execute_query(query), query

    def avg_fuel_cost_by_road_type_and_month(self) -> (pd.DataFrame, str):
        """
        Calculate average fuel cost by road type and month.
        Returns a DataFrame with columns: road_type, month, year, avg_fuel_cost, total_distance.
        """
        query = """
        SELECT
            dr.road_type,
            dd.month,
            dd.year,
            AVG(df.price_per_liter * fvu.fuel_consumption) as avg_fuel_cost,
            SUM(fvu.distance_km) as total_distance
        FROM dim_route dr
        JOIN fact_vehicle_usage fvu ON dr.route_id = fvu.route_id
        JOIN dim_fuel df ON fvu.fuel_id = df.fuel_id
        JOIN dim_date dd ON fvu.date_id = dd.date_id
        GROUP BY dr.road_type, dd.month, dd.year
        ORDER BY dd.year, dd.month, avg_fuel_cost DESC;
        """
        return self.execute_query(query), query

    def most_risky_routes_by_incidents(self, top: int = 5) -> (pd.DataFrame, str):
        """
        Identify routes with the highest number of incidents and their cost impact.
        Returns a DataFrame with columns: start_location, end_location, incident_count, total_cost_impact.
        """
        query = f"""
        SELECT
            dr.start_location,
            dr.end_location,
            COUNT(di.incident_id) as incident_count,
            SUM(di.cost_impact) as total_cost_impact
        FROM dim_route dr
        JOIN fact_shipments fs ON dr.route_id = fs.route_id
        JOIN dim_incident di ON fs.shipment_id = di.shipment_id
        GROUP BY dr.route_id, dr.start_location, dr.end_location
        ORDER BY incident_count DESC, total_cost_impact DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

    def driver_efficiency_trends(self, top: int = 5) -> (pd.DataFrame, str):
        """
        Analyze trends in driver efficiency over time (shipments per month).
        First select top N drivers based on total shipment count, then retrieve all their monthly records.
        Returns a DataFrame with columns: first_name, last_name, month, year, shipment_count, previous_month_shipments, shipment_diff.
        """
        # Step 1: Select top N drivers based on total shipment count
        query_top_drivers_comment = "Step 1: Select top N drivers based on total shipment count"
        query_top_drivers = f"""
        SELECT
            dd.driver_id,
            dd.first_name,
            dd.last_name,
            SUM(COUNT(fs.shipment_id)) OVER (PARTITION BY dd.driver_id) as total_shipments
        FROM dim_driver dd
        JOIN fact_shipments fs ON dd.driver_id = fs.driver_id
        GROUP BY dd.driver_id, dd.first_name, dd.last_name
        ORDER BY total_shipments DESC
        LIMIT {top};
        """
        top_drivers_df = self.execute_query(query_top_drivers)
        top_driver_ids = tuple(top_drivers_df['driver_id'].tolist()) if not top_drivers_df.empty else (0,)

        # Step 2: Retrieve all monthly records for the selected drivers
        query_comment = "#Step 2: Retrieve all monthly records for the selected drivers"
        query = f"""
        WITH monthly_shipments AS (
            SELECT
                dd.driver_id,
                dd.first_name,
                dd.last_name,
                dt.month,
                dt.year,
                COUNT(fs.shipment_id) as shipment_count
            FROM dim_driver dd
            JOIN fact_shipments fs ON dd.driver_id = fs.driver_id
            JOIN dim_date dt ON fs.date_id = dt.date_id
            WHERE dd.driver_id IN {top_driver_ids}
            GROUP BY dd.driver_id, dd.first_name, dd.last_name, dt.month, dt.year
        ),
        ranked_drivers AS (
            SELECT
                first_name,
                last_name,
                month,
                year,
                shipment_count,
                LAG(shipment_count) OVER (PARTITION BY first_name, last_name ORDER BY year, month) as previous_month_shipments,
                (shipment_count - LAG(shipment_count) OVER (PARTITION BY first_name, last_name ORDER BY year, month)) as shipment_diff
            FROM monthly_shipments
        )
        SELECT
            first_name,
            last_name,
            month,
            year,
            shipment_count,
            previous_month_shipments,
            shipment_diff
        FROM ranked_drivers
        WHERE shipment_count > 0
        ORDER BY year, month;
        """
        return self.execute_query(query), f"{query_top_drivers_comment}\n{query_top_drivers}\n{query_comment}\n{query}"

    def route_distances(self, top: int = 5) -> (pd.DataFrame, str):
        """
        Calculate actual geographic distances between start and end locations in dim_route using PostGIS ST_Distance.
        Returns a DataFrame with columns: start_location, end_location, geographic_distance_km.
        """
        query = f"""
        SELECT
            start_location,
            end_location,
            ST_Distance(
                ST_SetSRID(ST_MakePoint(start_longitude, start_latitude), 4326)::geography,
                ST_SetSRID(ST_MakePoint(end_longitude, end_latitude), 4326)::geography
            ) / 1000 as geographic_distance_km
        FROM dim_route
        ORDER BY geographic_distance_km DESC
        LIMIT {top};
        """
        return self.execute_query(query), query

def run_all_queries():
    queries = LogisticsQueries()
    results = {}

    print("\nQuery 1: Average delivery time by customer's city")
    results['avg_delivery_time_by_city'] = queries.avg_delivery_time_by_city()
    print(results['avg_delivery_time_by_city'])

    print("\nQuery 2: Most frequently used drivers (by number of shipments)")
    results['most_frequent_drivers'] = queries.most_frequent_drivers()
    print(results['most_frequent_drivers'])

    print("\nQuery 3: Fuel costs per vehicle usage")
    results['fuel_costs_per_vehicle_usage'] = queries.fuel_costs_per_vehicle_usage()
    print(results['fuel_costs_per_vehicle_usage'])

    print("\nQuery 4: Total weight shipped per warehouse")
    results['total_weight_per_warehouse'] = queries.total_weight_per_warehouse()
    print(results['total_weight_per_warehouse'])

    print("\nQuery 5: Most expensive shipments by shipping cost")
    results['most_expensive_shipments'] = queries.most_expensive_shipments()
    print(results['most_expensive_shipments'])

    print("\nQuery 6: Incidents by type and their total cost impact")
    results['incidents_by_type'] = queries.incidents_by_type()
    print(results['incidents_by_type'])

    print("\nQuery 7: Delivery time trends by month")
    results['delivery_time_trends_by_month'] = queries.delivery_time_trends_by_month()
    print(results['delivery_time_trends_by_month'])

    print("\nQuery 8: Driver ranking by average delivery time")
    results['driver_ranking_by_delivery_time'] = queries.driver_ranking_by_delivery_time()
    print(results['driver_ranking_by_delivery_time'])

    print("\nQuery 9: Monthly delivery time changes")
    results['monthly_delivery_time_changes'] = queries.monthly_delivery_time_changes()
    print(results['monthly_delivery_time_changes'])

    print("\nQuery 10: Incidents distribution over time")
    results['incidents_distribution_over_time'] = queries.incidents_distribution_over_time()
    print(results['incidents_distribution_over_time'])

    print("\nQuery 11: Delivery time percentiles by vehicle type")
    results['delivery_time_percentiles_by_vehicle_type'] = queries.delivery_time_percentiles_by_vehicle_type()
    print(results['delivery_time_percentiles_by_vehicle_type'])

    print("\nQuery 12: Average fuel cost by road type and month")
    results['avg_fuel_cost_by_road_type_and_month'] = queries.avg_fuel_cost_by_road_type_and_month()
    print(results['avg_fuel_cost_by_road_type_and_month'])

    print("\nQuery 13: Most risky routes by incidents")
    results['most_risky_routes_by_incidents'] = queries.most_risky_routes_by_incidents()
    print(results['most_risky_routes_by_incidents'])

    print("\nQuery 14: Driver efficiency trends")
    results['driver_efficiency_trends'] = queries.driver_efficiency_trends()
    print(results['driver_efficiency_trends'])

    return results

if __name__ == "__main__":
    run_all_queries()