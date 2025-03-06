# file: src/pages/most_expensive_shipments.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Najdroższe przesyłki"
    purpose = "Analiza ta pokazuje przesyłki z najwyższymi kosztami wysyłki, co może pomóc w identyfikacji kosztownych tras lub typów pojazdów."

    top_n = get_top_n_slider(key="most_expensive_top_n")
    city_filter = get_city_filter(key="most_expensive_city_filter")

    df, query_code = queries.most_expensive_shipments(top=top_n)
    if city_filter:
        df = df[df['start_location'].isin(city_filter) | df['end_location'].isin(city_filter)]

    fig = None
    if not df.empty:
        fig = create_bar_chart(df, x='shipping_cost', y='start_location', color='end_location',
                               title="Najdroższe przesyłki",
                               x_label="Koszt wysyłki (PLN)", y_label="Miasto początkowe")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Miasto docelowe")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Top N": top_n, "Filtr miast": ", ".join(city_filter) if city_filter else "Brak"},
            "data": df, "plot": fig}