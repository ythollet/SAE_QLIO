import streamlit as st
from datetime import date


def func_date_filter(key: str = "date_filter"):
    """
    Filtre de période affiché dans la sidebar (bandeau gauche).
    Retourne (date_debut, date_fin) ou (None, None) si la plage est invalide.
    """
    st.sidebar.markdown("### Filtre de période")

    date_debut = st.sidebar.date_input(
        "Date de début",
        value=date(2023, 1, 1),
        key=f"{key}_debut"
    )
    date_fin = st.sidebar.date_input(
        "Date de fin",
        value=date.today(),
        key=f"{key}_fin"
    )

    if date_debut > date_fin:
        st.sidebar.error("La date de début doit être antérieure à la date de fin.")
        return None, None

    return date_debut, date_fin
