# file: src/pages/fuel_costs_per_vehicle_usage.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Koszty paliwa według użycia pojazdu"
    purpose = "Analiza ta oblicza koszty paliwa dla każdego użycia pojazdu, co pozwala na identyfikację najbardziej kosztownych pojazdów i typów paliwa."

    top_n = get_top_n_slider(key="fuel_costs_top_n")
    df, query_code = queries.fuel_costs_per_vehicle_usage(top=top_n)

    fig = None
    if not df.empty:
        fig = create_bar_chart(df, x='total_fuel_cost', y='vehicle_type', color='fuel_type',
                               title="Koszty paliwa według użycia pojazdu",
                               x_label="Całkowity koszt paliwa (PLN)", y_label="Typ pojazdu")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Typ paliwa")

    return {"title": title, "purpose": purpose, "query_code": query_code, "filters": {"Top N": top_n},
            "data": df, "plot": fig}