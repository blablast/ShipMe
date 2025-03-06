# file: src/pages/incidents_by_type.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Incydenty według typu"
    purpose = "Analiza ta pozwala zrozumieć, jakie typy incydentów występują najczęściej oraz jaki jest ich całkowity wpływ kosztowy. Pomaga w podejmowaniu decyzji o zapobieganiu najczęstszym problemom."

    top_n = get_top_n_slider(key="incidents_by_type_top_n")
    df, query_code = queries.incidents_by_type(top=top_n)

    fig = None
    if not df.empty:
        fig = create_bar_chart(df, x='total_cost_impact', y='incident_type', title="Incydenty według typu",
                               x_label="Całkowity wpływ kosztowy (PLN)", y_label="Typ incydentu")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5))

    return {"title": title, "purpose": purpose, "query_code": query_code, "filters": {"Top N": top_n},
            "data": df, "plot": fig}