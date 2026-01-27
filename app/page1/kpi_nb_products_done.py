import streamlit as st
from utils.cnx_sql import func_query_sql_df


def func_kpi_nb_products_done():

    query = """
    SELECT 
	    COUNT(*) as nb_produits_termines
    FROM `tblfinorder` 
    WHERE TIMESTAMPDIFF(YEAR,DATE(Start),CURDATE()) < 1


    """

    df_nb_produits_termines = func_query_sql_df(query)

    nb_produits_temines = df_nb_produits_termines.iloc[0,0]

    st.metric(
        label = "Produits Terminés (dernière année)", 
        value = nb_produits_temines
    )