# file: src/templates/display_template.py
import streamlit as st

def render_page(content) :
    """
    Render a page with a standard layout based on the provided content.
    Content should be a dictionary with the following keys:
    - title: Title of the page
    - purpose: Purpose of the analysis (description)
    - query_code: SQL query code (optional)
    - data: DataFrame with results (optional)
    - plot: Plotly figure or None
    - additional_content: Additional HTML/Markdown content (optional)
    """
    # Header
    st.header(content['title'])
    st.markdown(content['purpose'])

    # Plot & table
    if content.get('plot') :
        st.plotly_chart(content['plot'])

    # Query code (if provided)
    if content.get('query_code') :
        st.markdown("#### Kod zapytania")
        st.code(content['query_code'], language = "sql")

    if content.get('data') is not None and not content['data'].empty :
        st.dataframe(content['data'])
    elif content.get('data') is not None :
        st.write("Brak danych do wyświetlenia.")


    # Additional content (e.g., for schema pages)
    if content.get('additional_content') :
        st.markdown(content['additional_content'], unsafe_allow_html = True)
