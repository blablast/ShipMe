# file: src/pages/readme_page.py

import streamlit as st

def get_page_content():
    st.header("Dokumentacja projektu")
    st.markdown("Poniżej znajduje się treść dokumentacji projektu (plik README.md):")

    # Wczytaj treść README.md
    try:
        with open("README.md", "r", encoding="utf-8") as file:
            readme_content = file.read()
        st.markdown(readme_content)
    except FileNotFoundError:
        st.warning("Plik README.md nie został znaleziony w głównym katalogu projektu. Upewnij się, że plik istnieje.")

    # About the author
    st.markdown("---")
    st.subheader("About the Author")
    col1, col2 = st.columns([1, 3])
    with col1 :
        st.image(
            "https://media.licdn.com/dms/image/v2/D4E03AQE7JnBb64dkPA/profile-displayphoto-shrink_200_200/B4EZVtsmKAHUAY-/0/1741302162624?e=1746662400&v=beta&t=BFSbvrgNMpQ0bvhhxjm1mu-6Iot6zdZ1u_7HTS1hrco")
    with col2 :
        st.markdown("""
            **Blazej Strus**  
            Data Scientist | Machine Learning Enthusiast  
            Experienced in developing machine learning models and implementing NLP solutions.

            📫 [b.strus@gmail.com](mailto:b.strus@gmail.com)   
            🌐 [LinkedIn](https://www.linkedin.com/in/b%C5%82a%C5%BCej-strus-7716192a/)
        """)