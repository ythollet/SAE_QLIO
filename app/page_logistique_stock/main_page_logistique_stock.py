from page_logistique_stock.kpi_encours_global import func_kpi_encours_global
from page_logistique_stock.barchart_encours_global import func_encours_global
from page_logistique_stock.barchart_taux_occupation_buffers import func_taux_occupation_buffers
import streamlit as st

def func_page_logistique_stock():


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
                "<h2 style='text-align: center;'> Occupation des buffers </h2>",
                unsafe_allow_html = True
            )

            with st.container(border = True):
                
                func_taux_occupation_buffers()
        
        with col2:

            st.markdown(
                "<h2 style='text-align: center;'> Encours Global </h2>",
                unsafe_allow_html = True
            )
            func_kpi_encours_global()

            
            with st.container(border = True):


                func_encours_global()