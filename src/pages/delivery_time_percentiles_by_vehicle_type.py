# file: src/pages/delivery_time_percentiles_by_vehicle_type.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Percentyle czasów dostaw według typu pojazdu"
    purpose = "Analiza ta pozwala ocenić rozkład czasów dostaw dla różnych typów pojazdów, pokazując medianę oraz 90. percentyl czasów dostaw."

    df, query_code = queries.delivery_time_percentiles_by_vehicle_type()

    fig = None
    if not df.empty:
        fig = create_bar_chart(df, x=['median_delivery_time', 'percentile_90_delivery_time'], y='vehicle_type',
                               title="Percentyle czasów dostaw według typu pojazdu",
                               x_label="Czas dostawy (godziny)", y_label="Typ pojazdu")
        fig.update_layout(barmode='group', legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Percentyl")

    return {"title": title, "purpose": purpose, "query_code": query_code, "filters": {}, "data": df, "plot": fig}