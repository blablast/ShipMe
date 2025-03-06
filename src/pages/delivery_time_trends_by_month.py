# file: src/pages/delivery_time_trends_by_month.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Trendy czasów dostaw według miesiąca"
    purpose = "Analiza ta pokazuje, jak średni czas dostawy zmienia się w czasie (według miesięcy i lat). Pomaga w identyfikacji trendów i anomalii w procesie dostaw."

    year_filter = get_year_filter(key="delivery_time_trends_year")
    month_filter = get_month_filter(key="delivery_time_trends_month")

    df, query_code = queries.delivery_time_trends_by_month()
    df = filter_by_year_month(df, year_filter, month_filter)

    fig = None
    if not df.empty:
        fig = create_line_chart(df, x='month', y='avg_delivery_time', color='year',
                                title="Trendy czasów dostaw według miesiąca",
                                x_label="Miesiąc", y_label="Średni czas dostawy (godziny)")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Rok")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Filtr lat": ", ".join(map(str, year_filter)) if year_filter else "Brak",
                        "Filtr miesięcy": ", ".join(map(str, month_filter)) if month_filter else "Brak"},
            "data": df, "plot": fig}