# file: src/pages/driver_efficiency_trends.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Trendy efektywności kierowców"
    purpose = "Analiza ta pokazuje, jak liczba przesyłek obsługiwanych przez kierowców zmienia się w czasie. Pomaga zidentyfikować kierowców z największym obciążeniem oraz trendy w ich efektywności."

    top_n = get_top_n_slider(label="Liczba kierowców", key="driver_efficiency_top_n")
    year_filter = get_year_filter(key="driver_efficiency_year")
    month_filter = get_month_filter(key="driver_efficiency_month")

    df, query_code = queries.driver_efficiency_trends(top=top_n)
    df['month'] = df['month'].astype(int)
    df['year'] = df['year'].astype(int)
    df['shipment_count'] = df['shipment_count'].astype(int)
    df['driver'] = df['first_name'] + ' ' + df['last_name']

    df = filter_by_year_month(df, year_filter, month_filter)

    fig = None
    if not df.empty:
        df = df.sort_values(by=['year', 'month'])
        fig = create_line_chart(df, x='month', y='shipment_count', color='driver', line_group='year',
                                title="Trendy efektywności kierowców",
                                x_label="Miesiąc", y_label="Liczba przesyłek", markers=True)
        fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                          legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                          legend_title="Kierowca")

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Liczba kierowców": top_n,
                        "Filtr lat": ", ".join(map(str, year_filter)) if year_filter else "Brak",
                        "Filtr miesięcy": ", ".join(map(str, month_filter)) if month_filter else "Brak"},
            "data": df, "plot": fig}