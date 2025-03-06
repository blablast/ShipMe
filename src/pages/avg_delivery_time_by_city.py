from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Średni czas dostawy według miasta"
    purpose = "Analiza ta ma na celu zidentyfikowanie miast, w których średni czas dostawy jest najdłuższy. Może to pomóc w optymalizacji procesów logistycznych w problematycznych lokalizacjach."

    top_n = get_top_n_slider(key="avg_delivery_time_top_n")
    city_filter = get_city_filter(table="dim_customer", column="city", key="avg_delivery_time_city_filter")

    df, query_code = queries.avg_delivery_time_by_city(top=top_n)
    if city_filter:
        df = df[df['city'].isin(city_filter)]

    fig = None
    if not df.empty:
        fig = create_bar_chart(df, x='avg_delivery_time', y='city', title="Średni czas dostawy według miasta",
                               x_label="Średni czas dostawy (godziny)", y_label="Miasto")

    return dict(title=title, purpose=purpose, query_code=query_code,
                filters={"Top N": top_n, "Filtr miast": ", ".join(city_filter) if city_filter else "Brak"},
                data=df, plot=fig)