import streamlit as st
from datetime import date


def func_date_filter(key: str = "date_filter"):
    """
    Widget filtre de période affiché en deux colonnes.
    Retourne (date_debut, date_fin) ou (None, None) si la plage est invalide.
    """
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        date_debut = st.date_input(
            "Date de début",
            value=date(2023, 1, 1),
            key=f"{key}_debut"
        )
    with col2:
        date_fin = st.date_input(
            "Date de fin",
            value=date.today(),
            key=f"{key}_fin"
        )
    if date_debut > date_fin:
        st.error("La date de début doit être antérieure à la date de fin.")
        return None, None
    return date_debut, date_fin
