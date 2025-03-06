# file: src/pages/geographic_distribution_of_routes.py
from .utils import *

def get_page_content():
    queries = LogisticsQueries()
    title = "Rozkład geograficzny tras"
    purpose = "Analiza ta pokazuje geograficzne rozłożenie tras między punktami początkowymi i końcowymi, co pozwala na ocenę ich zasięgu i rozmieszczenia."
    query_code = "SELECT route_id, start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude FROM dim_route"

    city_filter = get_city_filter(key="geo_routes_city_filter")
    df = queries.execute_query(query_code)
    if city_filter:
        df = df[df['start_location'].isin(city_filter) | df['end_location'].isin(city_filter)]

    fig = None
    if not df.empty:
        lines = [{'lat': [row['start_latitude'], row['end_latitude']],
                  'lon': [row['start_longitude'], row['end_longitude']],
                  'name': f"{row['start_location']} -> {row['end_location']}"} for _, row in df.iterrows()]
        fig = create_map_scatter(df, lat='start_latitude', lon='start_longitude', hover_name='start_location',
                                 title="Rozkład geograficzny tras")
        fig.add_scattermapbox(lat=df['end_latitude'], lon=df['end_longitude'], mode='markers',
                              marker=dict(size=20, color='red'))
        fig.update_layout(showlegend = False)
        for line in lines:
            fig.add_scattermapbox(lat=line['lat'], lon=line['lon'], mode='lines',
                                  line=dict(width=2, color='gray'))

    return {"title": title, "purpose": purpose, "query_code": query_code,
            "filters": {"Filtr miast": ", ".join(city_filter) if city_filter else "Brak"},
            "data": df, "plot": fig}