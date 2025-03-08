import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL

def get_page_content():
    # Connect to the database
    engine = create_engine(DATABASE_URL)

    # Get list of tables in the public schema
    query_tables = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE'
    AND (table_name LIKE 'dim_%' OR table_name LIKE 'fact_%')
    ORDER BY table_name;
    """
    with engine.connect() as connection:
        tables = connection.execute(text(query_tables)).fetchall()
        table_names = [row[0] for row in tables]

    # Count records for each dimension and fact table
    stats = []
    with engine.connect() as connection:
        for table in table_names:
            query_count = f"SELECT COUNT(*) FROM {table}"
            try:
                count = connection.execute(text(query_count)).scalar()
                stats.append({"Tabela": table, "Liczba rekordów": count})
            except Exception as e:
                st.error(f"Błąd podczas zliczania rekordów dla tabeli {table}: {e}")

    # Prepare data for display
    df = pd.DataFrame(stats) if stats else None
    plot = None
    if df is not None and not df.empty:
        # Create a bar chart using Plotly
        plot = px.bar(
            df,
            x="Tabela",
            y="Liczba rekordów",
            title="Liczba rekordów w tabelach",
            labels={"Liczba rekordów": "Liczba rekordów"},
            text=df["Liczba rekordów"].apply(lambda x: f"{x:,}"),  # Add comma separators to labels
            height=400
        )
        plot.update_traces(textposition="auto")  # Position labels automatically
        plot.update_layout(xaxis_tickangle=-45)  # Rotate x-axis labels for better readability

    # Prepare content for the render_page template
    content = {
        "title": "Statystyki bazy danych",
        "purpose": "Ta strona wyświetla listę tabel wymiarów (dim_) i faktów (fact_) w bazie danych wraz z liczbą rekordów.",
        "data": df,
        "query_code": None,  # SQL query can be added here if needed
        "plot": plot,
        "additional_content": "Nie znaleziono tabel wymiarów ani faktów w bazie danych lub wystąpił problem z połączeniem."  if not stats else None
    }

    return content