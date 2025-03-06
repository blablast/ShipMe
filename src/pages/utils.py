# file: src/pages/utils.py
import streamlit as st
import plotly.express as px
from src.analysis.queries import LogisticsQueries

def filter_by_year_month(df, year_filter=None, month_filter=None):
    if year_filter:
        df = df[df['year'].isin(year_filter)]
    if month_filter:
        df = df[df['month'].isin(month_filter)]
    return df

def get_top_n_slider(label="Top N wyników", min_value=1, max_value=100, value=5, key="top_n"):
    return st.slider(label=label, min_value=min_value, max_value=max_value, value=value, key=key)

def get_year_filter(label="Filtruj po roku", options=None, default=None, key="year_filter"):
    if options is None:
        options = list(range(2023, 2025))
    if default is None:
        default = [2023]
    return st.multiselect(label=label, options=options, default=default, key=key)

def get_month_filter(label="Filtruj po miesiącu", options=None, default=None, key="month_filter"):
    if options is None:
        options = list(range(1, 13))
    if default is None:
        default = list(range(1, 13))
    return st.multiselect(label=label, options=options, default=default, key=key)

def get_city_filter(label="Filtruj po mieście", table="dim_route", column="start_location", key="city_filter"):
    queries = LogisticsQueries()
    query = f"SELECT DISTINCT {column} FROM {table}"
    options = list(queries.execute_query(query)[column])
    return st.multiselect(label=label, options=options, key=key)

def create_bar_chart(df, x, y, color=None, title="Wykres słupkowy", x_label=None, y_label=None):
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    fig.update_layout(xaxis_title=x_label or x, yaxis_title=y_label or y)
    return fig

def create_line_chart(df, x, y, color=None, line_group=None, title="Wykres liniowy", x_label=None, y_label=None, markers=False):
    fig = px.line(df, x=x, y=y, color=color, line_group=line_group, title=title)
    if markers:
        fig.update_traces(mode='lines+markers')
    fig.update_layout(xaxis_title=x_label or x, yaxis_title=y_label or y)
    return fig

def create_map_scatter(df, lat, lon, hover_name, hover_data=None, title="Mapa", zoom=5, height=700):
    fig = px.scatter_mapbox(df, lat=lat, lon=lon, hover_name=hover_name, hover_data=hover_data, zoom=zoom, height=height, title=title)
    fig.update_layout(mapbox_style="open-street-map")
    df.drop(columns=["point_size"], inplace=True, errors="ignore")
    return fig