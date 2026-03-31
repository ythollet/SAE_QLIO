import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from utils.cnx_sql import func_query_sql_df


def func_kpi_cycle_termine():
    """Affiche le nombre de cycles terminés aujourd'hui avec comparaison aux 7 derniers jours."""
    query = """
    SELECT DATE(End) AS date, COUNT(DISTINCT ONo) AS nb_cycles
    FROM tblfinorderpos
    WHERE DATE(End) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    GROUP BY DATE(End);
    """

    try:
        df = func_query_sql_df(query)
        if df is not None and not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            today = pd.Timestamp.now().date()
            today_count = df[df['date'].dt.date == today]['nb_cycles'].sum() if not df[df['date'].dt.date == today].empty else 0
            prev_7_days = df[df['date'].dt.date < today]
            avg_prev = prev_7_days['nb_cycles'].mean() if not prev_7_days.empty else 0
            if avg_prev > 0:
                pct_change = ((today_count - avg_prev) / avg_prev) * 100
                vs_text = f"vs 7 derniers jours: {'+' if pct_change > 0 else ''}{pct_change:.1f}%"
                vs_color = '#4caf50' if pct_change > 0 else '#f44336'
            else:
                vs_text = "vs 7 derniers jours: N/A"
                vs_color = '#ff9800'
        else:
            today_count = 0
            vs_text = "vs 7 derniers jours: N/A"
            vs_color = '#ff9800'
    except Exception as e:
        st.warning(f"Impossible de récupérer le nombre de cycles terminés (BD): {e}")
        today_count = 0
        vs_text = "vs 7 derniers jours: N/A"
        vs_color = '#ff9800'

    # Code HTML pour le KPI
    html_kpi = f"""
    <div style="border: 2px solid #00d2b4; padding: 15px 20px 20px 20px; background-color: #1a1c23; width: 250px; height: 180px; border-radius: 4px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <div style="color: #9e9e9e; font-size: 12px; font-weight: 600; letter-spacing: 1px; margin-bottom: 5px;">
            CYCLE TERMINÉS DE LA JOURNÉE
        </div>
        <div style="color: white; font-size: 32px; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 5px;">
            {today_count}
        </div>
        <div style="color: {vs_color}; font-size: 12px; font-weight: 600;">
            {vs_text}
        </div>
    </div>
    """

    components.html(html_kpi, height=180)