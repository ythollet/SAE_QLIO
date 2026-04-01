import streamlit as st
from utils.date_filter import func_date_filter
from page_qualite.kpi_taux_de_rebut import func_kpi_taux_de_rebut
from page_qualite.barchart_top5_causes_nok import func_barchart_top5_causes_nok
from page_qualite.barchart_taux_conformite_par_of import func_barchart_taux_conformite_par_of

def func_page_qualite():

    date_debut, date_fin = func_date_filter(key="qualite")

    # Ligne du haut : stacked bar OF (gauche) + jauge taux de rebut (droite)
    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                func_barchart_taux_conformite_par_of()

        with col2:
            with st.container(border=True):
                func_kpi_taux_de_rebut(date_debut, date_fin)

    # Ligne du bas : Pareto pleine largeur
    with st.container(border=True):
        with st.container(border=True):
            func_barchart_top5_causes_nok(date_debut, date_fin)
