# file: src/pages/schema_fact_vehicle_usage.py

def get_page_content() :
    title = "Schemat tabeli Fact Vehicle Usage"
    purpose = """
    Tabela `fact_vehicle_usage` przechowuje dane o użyciu pojazdów, łącząc wymiary takie jak pojazd (`dim_vehicle`), kierowca (`dim_driver`), trasa (`dim_route`), paliwo (`dim_fuel`) i data (`dim_date`). Umożliwia analizę kosztów paliwa, dystansu i konserwacji pojazdów.
    """
    principles = """
    - Klucz główny: `usage_id`.
    - Klucze obce: `vehicle_id`, `driver_id`, `route_id`, `fuel_id`, `date_id`.
    - Każde użycie pojazdu jest powiązane z dokładnie jednym rekordem w każdym z wymiarów.
    - Kolumny `distance_km`, `fuel_consumption`, `maintenance_cost` przechowują dane ilościowe do analizy.
    """
    schema_iframe = """
    <iframe width="1000" height="500" src='https://dbdiagram.io/e/67c96837263d6cf9a06d0ae1/67c96d32263d6cf9a06dde34'></iframe>
    """

    return {"title" : title, "purpose" : purpose, "query_code" : "", "filters" : {}, "data" : None, "plot" : None,
        "additional_content" : f"""
        ### Zasady projektowe
        {principles}
        ### Schemat w dbdiagram.io
        {schema_iframe}
        """}