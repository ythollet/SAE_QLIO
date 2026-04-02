import streamlit as st
from utils.top_banner import func_top_banner
from page_qualite.kpi_taux_de_rebut import func_kpi_taux_de_rebut
from page_qualite.barchart_top5_causes_nok import func_barchart_top5_causes_nok
from page_qualite.barchart_taux_conformite_par_of import func_barchart_taux_conformite_par_of

def func_page_qualite():

    date_debut, date_fin = func_top_banner(key="qualite")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                func_barchart_taux_conformite_par_of()
        with col2:
            with st.container(border=True):
                func_kpi_taux_de_rebut(date_debut, date_fin)

    with st.container(border=True):
        func_barchart_top5_causes_nok(date_debut, date_fin)
