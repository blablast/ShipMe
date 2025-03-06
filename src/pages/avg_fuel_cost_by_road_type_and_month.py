# file: src/pages/avg_fuel_cost_by_road_type_and_month.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Średni koszt paliwa według typu drogi i miesiąca"
    purpose = "Analiza ta pozwala zobaczyć, jak średni koszt paliwa zmienia się w zależności od typu drogi i miesiąca, co może pomóc w optymalizacji tras."

    year_filter = get_year_filter(key="avg_fuel_cost_year")
    month_filter = get_month_filter(key="avg_fuel_cost_month")

    df, query_code = queries.avg_fuel_cost_by_road_type_and_month()
    df = filter_by_year_month(df, year_filter, month_filter)

    fig = None
    if not df.empty:
        fig = create_line_chart(df, x='month', y='avg_fuel_cost', color='road_type', line_group='year',
                                title="Średni koszt paliwa według typu drogi i miesiąca",
                                x_label="Miesiąc", y_label="Średni koszt paliwa (PLN)")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Typ drogi")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Filtr lat": ", ".join(map(str, year_filter)) if year_filter else "Brak",
                        "Filtr miesięcy": ", ".join(map(str, month_filter)) if month_filter else "Brak"},
            "data": df, "plot": fig}