import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from utils.cnx_sql import func_query_sql_df


def func_kpi_cycle_termine(date_debut=None, date_fin=None):
    """Affiche le nombre de cycles terminés sur la période avec comparaison aux 7 jours précédents."""

    if date_debut:
        filtre = f"WHERE DATE(End) BETWEEN '{date_debut}' AND '{date_fin}'"
    else:
        filtre = "WHERE DATE(End) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"

    query = f"""
    SELECT DATE(End) AS date, COUNT(DISTINCT ONo) AS nb_cycles
    FROM tblfinorderpos
    {filtre}
    GROUP BY DATE(End);
    """

    try:
        df = func_query_sql_df(query)
        if df is not None and not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            total_count = int(df['nb_cycles'].sum())
            avg_per_day = df['nb_cycles'].mean()
            nb_jours = df['date'].nunique()
            vs_text = f"Sur {nb_jours} jour(s) — moy. {avg_per_day:.1f}/j"
            vs_color = '#4caf50'
        else:
            total_count = 0
            vs_text = "Aucune donnée sur cette période"
            vs_color = '#ff9800'
    except Exception as e:
        st.warning(f"Impossible de récupérer le nombre de cycles terminés (BD): {e}")
        total_count = 0
        vs_text = "Erreur de chargement"
        vs_color = '#f44336'

    html_kpi = f"""
    <div style="border: 2px solid #00d2b4; padding: 15px 20px 20px 20px; background-color: #1a1c23; width: 250px; height: 180px; border-radius: 4px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <div style="color: #9e9e9e; font-size: 12px; font-weight: 600; letter-spacing: 1px; margin-bottom: 5px;">
            CYCLES TERMINÉS
        </div>
        <div style="color: white; font-size: 32px; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 5px;">
            {total_count}
        </div>
        <div style="color: {vs_color}; font-size: 12px; font-weight: 600;">
            {vs_text}
        </div>
    </div>
    """

    components.html(html_kpi, height=180)
