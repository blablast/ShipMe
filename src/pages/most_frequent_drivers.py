# file: src/pages/most_frequent_drivers.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Najczęściej używani kierowcy"
    purpose = "Analiza ta pozwala zidentyfikować kierowców, którzy obsługują największą liczbę przesyłek. Pomaga w zrozumieniu obciążenia pracą i potencjalnego ryzyka przeciążenia."

    top_n = get_top_n_slider(key="most_frequent_drivers_top_n")
    df, query_code = queries.most_frequent_drivers(top=top_n)
    if df is not None and not df.empty:
        df['driver'] = df['first_name'] + ' ' + df['last_name']

    fig = None
    if df is not None and not df.empty:
        fig = create_bar_chart(df, x='shipment_count', y='driver', title="Najczęściej używani kierowcy",
                               x_label="Liczba przesyłek", y_label="Kierowca")
        fig.update_layout(legend_title="")

    return {"title": title, "purpose": purpose, "query_code": query_code, "filters": {"Top N": top_n},
            "data": df, "plot": fig}