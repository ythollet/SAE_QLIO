import streamlit as st
import mysql.connector
import pandas as pd 
from page1.barchart_nb_produits_termines_par_jour import *
from page1.linechart_temps_moyen_cycle import *
from page1.kpi_temps_moyen_cycle import *
from page1.kpi_nb_produits_termines import *
from utils.cnx_sql import func_query_sql_df

# La configuration de la page doit être la première commande Streamlit
st.set_page_config(layout='wide')


def func_page1():

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

pages = [
    st.Page(func_page1, title = 'Page 1', icon = "📊")
]

app = st.navigation(pages)

app.run()