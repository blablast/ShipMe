# file: src/pages/monthly_delivery_time_changes.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Zmiany czasów dostaw w miesiącach"
    purpose = "Analiza ta pozwala zobaczyć, jak średni czas dostawy zmienia się z miesiąca na miesiąc, co może wskazywać na trendy lub problemy w procesie dostaw."

    year_filter = get_year_filter(key="monthly_delivery_year")
    month_filter = get_month_filter(key="monthly_delivery_month")

    df, query_code = queries.monthly_delivery_time_changes()
    df = filter_by_year_month(df, year_filter, month_filter)

    fig = None
    if not df.empty:
        fig = create_line_chart(df, x='month', y='time_diff', color='year', title="Zmiany czasów dostaw w miesiącach",
                                x_label="Miesiąc", y_label="Różnica czasu dostawy (godziny)")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Rok")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Filtr lat": ", ".join(map(str, year_filter)) if year_filter else "Brak",
                        "Filtr miesięcy": ", ".join(map(str, month_filter)) if month_filter else "Brak"},
            "data": df, "plot": fig}