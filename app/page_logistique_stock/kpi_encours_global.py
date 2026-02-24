from utils.cnx_sql import func_query_sql_df
import streamlit as st
import altair as alt
import pandas as pd   


def func_kpi_encours_global():

    query_nb_ordres_en_cours = """
        SELECT 
            COUNT(*)
        FROM tblfinorder
        WHERE End is NULL
    """
    nb_ordres_en_cours = func_query_sql_df(query_nb_ordres_en_cours).iloc[0,0]

    query_nb_pieces_en_buffer = """
        SELECT 
            COUNT(*) as nb_pieces_buffer
        FROM tblbufferpos as bpos
        WHERE PNo <> 0
    """
    nb_pieces_en_buffer = func_query_sql_df(query_nb_pieces_en_buffer).iloc[0,0]

    col1, col2 = st.columns(2)
    col1.metric("Ordres en cours", nb_ordres_en_cours)
    col2.metric("Pièces en buffer", nb_pieces_en_buffer)