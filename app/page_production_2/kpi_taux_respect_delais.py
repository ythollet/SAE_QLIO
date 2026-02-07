import streamlit as st
from utils.cnx_sql import func_query_sql_df
import pandas as pd 
from datetime import datetime
from dateutil.relativedelta import relativedelta
import altair as alt

def func_kpi_taux_respect_delais():

    query = """
        SELECT 
            CAST(ROUND(SUM(CASE WHEN End <= PlannedEnd THEN 1 else 0 END) / COUNT(*) * 100, 0) as SIGNED) as pct_respect_delais
        FROM `tblfinorder`
    """

    df = func_query_sql_df(query)

    taux_respect_delais = df.iloc[0,0]

    taux_cible = 90

    st.metric(
        label = "Taux de Respect des Délais",
        value = f"{taux_respect_delais} %",
        delta="Objectif atteint" if taux_respect_delais >= taux_cible else "Sous l'objectif",
        delta_color="normal" if taux_respect_delais >= taux_cible else "inverse"
        )