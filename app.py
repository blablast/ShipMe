# file: app.py
import streamlit as st
import pandas as pd

# Set global settings
st.set_page_config(page_title="Ship Me Dashboard", page_icon="🚛", layout="wide")
pd.options.display.float_format = '{:,.2f}'.format

# Import pages
from src.pages import *

# Import display template
from src.templates.display_template import render_page

# Initialize session state for storing selected analysis
if 'selected_analysis_key' not in st.session_state:
    st.session_state.selected_analysis_key = None

# Sidebar navigation
st.sidebar.header("Wybierz analizę")
# Grouped analyses with short descriptions
grouped_analyses = {"📅 Analizy czasowe" : sorted([
    {"key" : "avg_fuel_cost", "title" : "Średni koszt paliwa według typu drogi i miesiąca",
     "content_func" : avg_fuel_cost_content},
    {"key" : "delivery_time_trends", "title" : "Trendy czasów dostaw według miesiąca",
     "content_func" : delivery_time_trends_content},
    {"key" : "driver_efficiency", "title" : "Trendy efektywności kierowców",
     "content_func" : driver_efficiency_content},
    {"key" : "incidents_distribution", "title" : "Rozkład incydentów w czasie",
     "content_func" : incidents_distribution_content},
    {"key" : "monthly_delivery_changes", "title" : "Zmiany czasów dostaw w miesiącach",
     "content_func" : monthly_delivery_changes_content}, ], key = lambda x : x["title"]),

    "🚛 Analizy transportowe" : sorted([{"key" : "avg_delivery_time", "title" : "Średni czas dostawy według miasta",
                                        "content_func" : avg_delivery_time_content},
        {"key" : "delivery_percentiles", "title" : "Percentyle czasów dostaw według typu pojazdu",
         "content_func" : delivery_percentiles_content},
        {"key" : "driver_ranking", "title" : "Ranking kierowców według czasu dostawy",
         "content_func" : driver_ranking_content},
        {"key" : "fuel_costs", "title" : "Koszty paliwa według użycia pojazdu", "content_func" : fuel_costs_content},
        {"key" : "most_expensive", "title" : "Najdroższe przesyłki", "content_func" : most_expensive_content},
        {"key" : "most_frequent_drivers", "title" : "Najczęściej używani kierowcy",
         "content_func" : most_frequent_drivers_content},
        {"key" : "most_risky_routes", "title" : "Najbardziej ryzykowne trasy według incydentów",
         "content_func" : most_risky_routes_content},
        {"key" : "route_distances", "title" : "Odległości tras (geograficzne)",
         "content_func" : route_distances_content}, ], key = lambda x : x["title"]),

    "🏬 Analizy magazynowe" : sorted(
        [{"key" : "total_weight", "title" : "Całkowita waga według magazynu", "content_func" : total_weight_content}, ],
        key = lambda x : x["title"]),

    "⚠️ Analizy incydentów" : sorted([
        {"key" : "incidents_by_type", "title" : "Incydenty według typu", "content_func" : incidents_by_type_content}, ],
        key = lambda x : x["title"]),

    "🗺️ Analizy geograficzne" : sorted(
        [{"key" : "geo_routes", "title" : "Rozkład geograficzny tras", "content_func" : geo_routes_content},
            {"key" : "geo_warehouses", "title" : "Rozkład geograficzny magazynów",
             "content_func" : geo_warehouses_content}, ], key = lambda x : x["title"]),

    "📜 Schematy" : sorted([{"key" : "schema_fact_shipments", "title" : "Schemat: Fact Shipments",
                            "content_func" : schema_fact_shipments_content},
        {"key" : "schema_fact_vehicle_usage", "title" : "Schemat: Fact Vehicle Usage",
         "content_func" : schema_fact_vehicle_usage_content},
        {"key" : "schema_fact_warehouse_activity", "title" : "Schemat: Fact Warehouse Activity",
         "content_func" : schema_fact_warehouse_activity_content}, ], key = lambda x : x["title"]),
}

st.markdown("""
    <style>
    div.stButton > button {
        width: 300px;  # Ustaw żądaną szerokość w pikselach
        display: inline-block;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Generate sidebar links grouped by category
selected_analysis = None
for group_name, analyses in grouped_analyses.items():
    st.sidebar.subheader(group_name)
    for analysis in analyses:
        if st.sidebar.button(f"**{analysis['title']}**", key=f"btn_{analysis['key']}"):
            st.session_state.selected_analysis_key = analysis['key']
            selected_analysis = analysis

# If no button clicked, restore from session state
if not selected_analysis and st.session_state.selected_analysis_key:
    for group_name, analyses in grouped_analyses.items():
        for analysis in analyses:
            if analysis['key'] == st.session_state.selected_analysis_key:
                selected_analysis = analysis
                break
        if selected_analysis:
            break

# Display selected analysis content
if selected_analysis:
    content = selected_analysis['content_func']()
    render_page(content)
else:
    st.image("docs/icon.png", width = 200)
    st.markdown('<span style="color: yellow;">Wybierz analizę z paska bocznego, aby zobaczyć szczegóły.</span>',
                unsafe_allow_html = True)
    # If no analysis selected, display readme page
    readme_content()