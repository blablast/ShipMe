# file: src/pages/schema_fact_warehouse_activity.py

def get_page_content() :
    title = "Schemat tabeli Fact Warehouse Activity"
    purpose = """
    Tabela `fact_warehouse_activity` przechowuje dane o aktywnościach magazynowych, łącząc wymiary takie jak produkt (`dim_product`), magazyn (`dim_warehouse`) i data (`dim_date`). Umożliwia analizę ruchów magazynowych i czasów przechowywania.
    """
    principles = """
    - Klucz główny: `activity_id`.
    - Klucze obce: `product_id`, `warehouse_id`, `date_id`.
    - Każda aktywność jest powiązana z dokładnie jednym rekordem w każdym z wymiarów.
    - Kolumny `stock_in`, `stock_out`, `storage_time` przechowują dane ilościowe do analizy.
    """
    schema_iframe = """
    <iframe width="1000" height="500" src='https://dbdiagram.io/e/67c96844263d6cf9a06d0c9c/67c96d5e263d6cf9a06de4e1'></iframe>
    """

    return {"title" : title, "purpose" : purpose, "query_code" : "", "filters" : {}, "data" : None, "plot" : None,
            "additional_content" : f"""
        ### Zasady projektowe
        {principles}
        ### Schemat w dbdiagram.io
        {schema_iframe}
        """}
