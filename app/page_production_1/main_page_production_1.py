import streamlit as st
from page_production_1.barchart_nb_produits_termines_par_jour import *
from page_production_1.linechart_temps_moyen_cycle import *
from page_production_1.kpi_temps_moyen_cycle import *
from page_production_1.kpi_nb_produits_termines import *

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
    """, 
    unsafe_allow_html = True
    )

    with st.container(border = True): 

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "<h2 style='text-align: center;'> Quantité Produite </h2>",
                unsafe_allow_html = True
            )

            with st.container(border = True):
                
                func_kpi_nb_produits_termines()

                func_barchart_nb_produits_termines_par_jour()
        
        with col2:

            st.markdown(
                "<h2 style='text-align: center;'> Durée Cycle </h2>",
                unsafe_allow_html = True
            )
            
            with st.container(border = True):

                func_kpi_temps_moyen_cycle()

                func_linechart_temps_moyen_cycle()