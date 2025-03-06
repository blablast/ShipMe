# file: src/pages/geographic_distribution_of_warehouses.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Rozkład geograficzny magazynów"
    purpose = "Analiza ta pokazuje lokalizację geograficzną magazynów na mapie, co pozwala na ocenę ich rozmieszczenia w Polsce."
    query_code = "SELECT warehouse_name, city, latitude, longitude FROM dim_warehouse"

    city_filter = get_city_filter(table="dim_warehouse", column="city", key="geo_warehouses_city_filter")
    df = queries.execute_query(query_code)
    if city_filter:
        df = df[df['city'].isin(city_filter)]

    fig = None
    if not df.empty:
        fig = create_map_scatter(df, lat='latitude', lon = 'longitude', hover_name = 'warehouse_name',
                                 hover_data=['city'], title="Rozkład geograficzny magazynów")
        fig.add_scattermapbox(lat=df['latitude'], lon=df['longitude'], mode='markers', marker=dict(size=20, color='red'))
        fig.update_layout(showlegend = False)

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Filtr miast": ", ".join(city_filter) if city_filter else "Brak"},
            "data": df, "plot": fig}