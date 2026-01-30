import streamlit as st
from utils.cnx_sql import func_query_sql_df

def func_linechart_duree_moyenne_en_buffer():

    query = """
        SELECT * 
        FROM tblfinorderpos INNER JOIN tblbuffer
	        ON tblfinorderpos.ResourceID = tblbuffer.ResourceId
    """

    # !! impossible a caluler car dans la table tblfinorderpos, 
    # ressourceID vaut toujours 0. Par conséquent la jointure entre 
    # les deux tables ne renvoie rien

    df = func_query_sql_df(query)