# file: src/pages/schema_fact_shipments.py

def get_page_content() :
    title = "Schemat tabeli Fact Shipments"
    purpose = """
    Tabela `fact_shipments` przechowuje dane o przesyłkach i jest centralnym elementem hurtowni danych. Łączy wymiary takie jak klient (`dim_customer`), trasa (`dim_route`), pojazd (`dim_vehicle`), kierowca (`dim_driver`), magazyn (`dim_warehouse`) i data (`dim_date`). Umożliwia analizę czasów dostaw, kosztów wysyłki i wagi przesyłek.
    """
    principles = """
    - Klucz główny: `shipment_id`.
    - Klucze obce: `customer_id`, `route_id`, `vehicle_id`, `driver_id`, `warehouse_id`, `date_id`.
    - Każda przesyłka jest powiązana z dokładnie jednym rekordem w każdym z wymiarów.
    - Kolumny `weight`, `shipping_cost`, `delivery_time` przechowują dane ilościowe do analizy.
    """
    schema_iframe = """
    <iframe width="1000" height="700" src='https://dbdiagram.io/e/67c94cc6263d6cf9a068ffd0/67c96b18263d6cf9a06d8688'></iframe>
    """

    return {"title" : title, "purpose" : purpose, "query_code" : "",  # Brak kodu SQL w schematach
        "filters" : {},  # Brak filtrów
        "data" : None,  # Brak tabeli danych
        "plot" : None,  # Brak wykresu
        "additional_content" : f"""
        ### Zasady projektowe
        {principles}
        ### Schemat w dbdiagram.io
        {schema_iframe}
        """}