from utils.cnx_sql import func_query_sql_df
import streamlit as st

def func_kpi_cycle_moyen():

    query = """
        SELECT 
            AVG(TIMESTAMPDIFF(SECOND,Start,End)) as temps_cycle_moyen
        FROM `tblfinorder` 
        WHERE TIMESTAMPDIFF(DAY,DATE(Start),CURDATE()) <= 100
    """

    df_temps_cycle_moyen = func_query_sql_df(query)

    temps_cycle_moyen_float = df_temps_cycle_moyen.iloc[0,0]

    minutes, secondes = divmod(temps_cycle_moyen_float, 60)

    temps_cycle_moyen_str = f"{int(minutes)} min {int(secondes)} sec"

    st.metric(
        label = "Durée Moyenne d'un Cycle (dernier mois)", 
        value = temps_cycle_moyen_str
    )