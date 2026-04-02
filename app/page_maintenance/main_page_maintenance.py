import streamlit as st
from utils.top_banner import func_top_banner
from page_maintenance.kpi_statut_system import func_kpi_statut_system
from page_maintenance.kpi_types_interventions import func_kpi_types_interventions
from page_maintenance.kpi_cycle_termine import func_kpi_cycle_termine


def func_page_maintenance():

    date_debut, date_fin = func_top_banner(key="maintenance")

    cols1 = st.columns(2)
    with cols1[0]:
        func_kpi_statut_system()
    with cols1[1]:
        func_kpi_cycle_termine(date_debut, date_fin)

    st.markdown("---")

    func_kpi_types_interventions(date_debut, date_fin)
