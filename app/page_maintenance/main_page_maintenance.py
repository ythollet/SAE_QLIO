import streamlit as st
from utils.date_filter import func_date_filter
from page_maintenance.kpi_statut_system import func_kpi_statut_system
from page_maintenance.kpi_types_interventions import func_kpi_types_interventions
from page_maintenance.kpi_cycle_termine import func_kpi_cycle_termine


def func_page_maintenance():
    st.markdown("## Maintenance")

    # Filtre de période
    func_date_filter(key="maintenance")

    # Première ligne : Statut système et Cycles terminés
    cols1 = st.columns(2)
    with cols1[0]:
        func_kpi_statut_system()
    with cols1[1]:
        func_kpi_cycle_termine()

    st.markdown("---")

    # Deuxième ligne : Graphique des interventions sur toute la largeur
    cols2 = st.columns(1)
    with cols2[0]:
        func_kpi_types_interventions()
