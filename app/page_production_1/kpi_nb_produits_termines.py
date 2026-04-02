import streamlit as st
from utils.cnx_sql import func_query_sql_df


def func_kpi_nb_produits_termines(date_debut=None, date_fin=None):

    filtre = (
        f"WHERE DATE(Start) BETWEEN '{date_debut}' AND '{date_fin}'"
        if date_debut
        else ""
    )

    query = f"""
    SELECT
        COUNT(*) as nb_produits_termines
    FROM `tblfinorder`
    {filtre}
    """

    df_nb_produits_termines = func_query_sql_df(query)

    nb_produits_temines = df_nb_produits_termines.iloc[0, 0]

    label = (
        f"Produits Terminés ({date_debut} → {date_fin})"
        if date_debut
        else "Produits Terminés (tout)"
    )

    st.metric(label=label, value=nb_produits_temines)
