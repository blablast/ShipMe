# file: src/pages/most_risky_routes_by_incidents.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Najbardziej ryzykowne trasy według incydentów"
    purpose = "Analiza ta pozwala zidentyfikować trasy z największą liczbą incydentów oraz ich kosztem. Pomaga w podejmowaniu decyzji o unikaniu ryzykownych tras lub wprowadzeniu dodatkowych środków bezpieczeństwa."

    top_n = get_top_n_slider(key="most_risky_routes_top_n")
    city_filter = get_city_filter(key="most_risky_routes_city_filter")

    df, query_code = queries.most_risky_routes_by_incidents(top=top_n)
    if city_filter:
        df = df[df['start_location'].isin(city_filter) | df['end_location'].isin(city_filter)]

    fig = None
    if df is not None and not df.empty:
        fig = create_bar_chart(df, x='incident_count', y='start_location', color='end_location',
                               title="Najbardziej ryzykowne trasy według incydentów",
                               x_label="Liczba incydentów", y_label="Miasto początkowe")
        fig.update_layout(legend_title="Miasto końcowe")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Top N": top_n, "Filtr miast": ", ".join(city_filter) if city_filter else "Brak"},
            "data": df, "plot": fig}