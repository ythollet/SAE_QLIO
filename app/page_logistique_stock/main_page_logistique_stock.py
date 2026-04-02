import streamlit as st
from utils.top_banner import func_top_banner
from page_logistique_stock.kpi_encours_global import func_kpi_encours_global
from page_logistique_stock.barchart_encours_global import func_encours_global
from page_logistique_stock.barchart_taux_occupation_buffers import func_taux_occupation_buffers

def func_page_logistique_stock():

    # Filtre affiché mais buffers = état courant (non filtrable par date)
    func_top_banner(key="logistique")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h2 style='text-align: center;'> Occupation des buffers </h2>", unsafe_allow_html=True)
            with st.container(border=True):
                func_taux_occupation_buffers()

        with col2:
            st.markdown("<h2 style='text-align: center;'> Encours Global </h2>", unsafe_allow_html=True)
            func_kpi_encours_global()
            with st.container(border=True):
                func_encours_global()
