# file: src/pages/total_weight_per_warehouse.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Całkowita waga według magazynu"
    purpose = "Analiza ta oblicza całkowitą wagę przesyłek według magazynu, co pozwala na ocenę obciążenia poszczególnych magazynów."

    top_n = get_top_n_slider(key="total_weight_top_n")
    city_filter = get_city_filter(table="dim_warehouse", column="city", key="total_weight_city_filter")

    df, query_code = queries.total_weight_per_warehouse(top=top_n)
    if city_filter:
        # Poprawka: filtrowanie po 'city', a nie 'warehouse_name'
        df_city = queries.execute_query("SELECT warehouse_name, city FROM dim_warehouse")
        df = df.merge(df_city, on='warehouse_name', how='left')
        df = df[df['city'].isin(city_filter)][['warehouse_name', 'total_weight']]

    fig = None
    if df is not None and not df.empty:
        fig = create_bar_chart(df, x='total_weight', y='warehouse_name', title="Całkowita waga według magazynu",
                               x_label="Całkowita waga (kg)", y_label="Nazwa magazynu")
        fig.update_layout(legend_title="")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Top N": top_n, "Filtr miast": ", ".join(city_filter) if city_filter else "Brak"},
            "data": df, "plot": fig}