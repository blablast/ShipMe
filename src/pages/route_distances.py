# file: src/pages/route_distances.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Odległości tras (geograficzne)"
    purpose = "Analiza ta oblicza rzeczywiste odległości geograficzne między punktami początkowymi i końcowymi tras, wykorzystując PostGIS ST_Distance."

    top_n = get_top_n_slider(key="route_distances_top_n")
    city_filter = get_city_filter(key="route_distances_city_filter")

    df, query_code = queries.route_distances(top=top_n)
    if city_filter:
        df = df[df['start_location'].isin(city_filter) | df['end_location'].isin(city_filter)]

    fig = None
    if df is not None and not df.empty:
        fig = create_bar_chart(df, x='geographic_distance_km', y='start_location', color='end_location',
                               title="Odległości tras (geograficzne)",
                               x_label="Odległość geograficzna (km)", y_label="Miasto początkowe")
        fig.update_layout(legend_title="Miasto końcowe")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Top N": top_n, "Filtr miast": ", ".join(city_filter) if city_filter else "Brak"},
            "data": df, "plot": fig}