# file: src/pages/driver_ranking_by_delivery_time.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Ranking kierowców według czasu dostawy"
    purpose = "Analiza ta pozwala ocenić kierowców pod kątem średniego czasu dostawy, co może pomóc w identyfikacji najbardziej efektywnych pracowników."
    top_n = get_top_n_slider(key="driver_ranking_top_n")

    df, query_code = queries.driver_ranking_by_delivery_time(top=top_n)
    df['driver'] = df['first_name'] + ' ' + df['last_name']

    fig = None
    if not df.empty:
        fig = create_bar_chart(df, x='avg_delivery_time', y='driver', title="Ranking kierowców według czasu dostawy",
                               x_label="Średni czas dostawy (godziny)", y_label="Kierowca")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5))

    return {"title": title, "purpose": purpose, "query_code": query_code, "filters": {"Top N": top_n},
            "data": df, "plot": fig}