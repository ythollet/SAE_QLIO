import streamlit as st
from utils.top_banner import func_top_banner
from page_production_1.barchart_nb_produits_termines_par_jour import func_barchart_nb_produits_termines_par_jour
from page_production_1.kpi_nb_produits_termines import func_kpi_nb_produits_termines
from page_production_1.barchart_trs import func_barchart_trs
from page_production_1.linechart_taux_fonctionnement import func_linechart_taux_fonctionnement

def func_page_production_1():

    date_debut, date_fin = func_top_banner(key="prod1")

    temps_planifie_h = st.sidebar.number_input(
        "Temps planifié / jour (h)",
        min_value=1, max_value=24, value=8, step=1,
        help="Utilisé pour le calcul du TRS et du Taux de Fonctionnement."
    )

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h2 style='text-align: center;'>Quantité Produite</h2>", unsafe_allow_html=True)
            with st.container(border=True):
                func_kpi_nb_produits_termines(date_debut, date_fin)
                func_barchart_nb_produits_termines_par_jour(date_debut, date_fin)
        with col2:
            st.markdown("<h2 style='text-align: center;'>TRS</h2>", unsafe_allow_html=True)
            with st.container(border=True):
                func_barchart_trs(temps_planifie_h, date_debut, date_fin)

    with st.container(border=True):
        func_linechart_taux_fonctionnement(temps_planifie_h, date_debut, date_fin)
