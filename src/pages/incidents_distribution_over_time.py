# file: src/pages/incidents_distribution_over_time.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Rozkład incydentów w czasie"
    purpose = "Analiza ta pokazuje, jak liczba incydentów zmienia się w czasie, co pozwala na identyfikację okresów o większym ryzyku."

    year_filter = get_year_filter(key="incidents_distribution_year")
    month_filter = get_month_filter(key="incidents_distribution_month")

    df, query_code = queries.incidents_distribution_over_time()
    if year_filter:
        df = df[df['incident_year'].isin(year_filter)]
    if month_filter:
        df = df[df['incident_month'].isin(month_filter)]

    fig = None
    if not df.empty:
        df = df.sort_values(by=['incident_year', 'incident_month'])
        fig = create_line_chart(df, x='incident_month', y='incident_count', color='incident_year',
                                title="Rozkład incydentów w czasie",
                                x_label="Miesiąc", y_label="Liczba incydentów", markers=True)
        fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                          legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Rok")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Filtr lat": ", ".join(map(str, year_filter)) if year_filter else "Brak",
                        "Filtr miesięcy": ", ".join(map(str, month_filter)) if month_filter else "Brak"},
            "data": df, "plot": fig}