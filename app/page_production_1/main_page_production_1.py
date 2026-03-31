import streamlit as st
from page_production_1.barchart_nb_produits_termines_par_jour import func_barchart_nb_produits_termines_par_jour
from page_production_1.kpi_nb_produits_termines import func_kpi_nb_produits_termines
from page_production_1.barchart_trs import func_barchart_trs
from page_production_1.linechart_taux_fonctionnement import func_linechart_taux_fonctionnement

def func_page_production_1():

    st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            display: flex;
            flex-direction: column;
            align-items: left;
            text-align: left;
            padding-left: 50px;
        }
        div[data-testid="stMetricLabel"] {
            text-align: center;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    # Paramètre temps planifié — colonne étroite pour ne pas prendre toute la largeur
    col_param, _ = st.columns([1, 3])
    with col_param:
        temps_planifie_h = st.number_input(
            "Temps planifié / jour (h)",
            min_value=1, max_value=24, value=8, step=1,
            help="Utilisé pour le calcul du Taux de Disponibilité (TRS) et du Taux de Fonctionnement."
        )

    # Ligne du haut : nb ordres/jour (gauche) + TRS décomposé (droite)
    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h2 style='text-align: center;'>Quantité Produite</h2>", unsafe_allow_html=True)
            with st.container(border=True):
                func_kpi_nb_produits_termines()
                func_barchart_nb_produits_termines_par_jour()

        with col2:
            st.markdown("<h2 style='text-align: center;'>TRS</h2>", unsafe_allow_html=True)
            with st.container(border=True):
                func_barchart_trs(temps_planifie_h)

    # Ligne du bas : évolution taux de fonctionnement
    with st.container(border=True):
        func_linechart_taux_fonctionnement(temps_planifie_h)
