import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit.components.v1 as components
from utils.cnx_sql import func_query_sql_df


def func_kpi_types_interventions():
    """Affiche un camembert Préventif vs Curatif et le total au centre."""
    query = """
    SELECT
        fo.Error,
        wpt.Description AS WorkPlantTypeName
    FROM tblfinorderpos fo
    LEFT JOIN tblworkplandef wpd ON fo.WPNo = wpd.WPNo
    LEFT JOIN tblworkplantype wpt ON wpd.Type = wpt.Type;
    """

    try:
        df = func_query_sql_df(query)
    except Exception as e:
        st.warning(f"Impossible de récupérer les types d'intervention (BD): {e}")
        # fallback mock data
        df = pd.DataFrame({
            'ID': [1, 2, 3, 4],
            'Error': [0, 1, 0, 2],
            'WorkPlantTypeName': ['Service', None, 'Autre', None]
        })

    if df is None or df.empty:
        # Zone d'erreur expliquant que le type d'intervention est manquant
        html_error = f"""
        <div style="border: 2px solid #ff4444; padding: 12px; background-color: #1a1c23; width: 700px; height: 190px; border-radius: 4px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0 auto;">
            <div style="color: #9e9e9e; font-size: 12px; font-weight: 600; letter-spacing: 1px; margin-bottom: 6px;">STATUT INTERVENTIONS</div>
            <div style="color: #ff4444; font-size: 14px;">Erreur: Le type d'intervention est une information manquante dans la base de données.</div>
        </div>
        """
        components.html(html_error, height=200)
        return
    def classify(row):
        wpt = row.get('WorkPlantTypeName')
        err = row.get('Error', 0)
        if isinstance(wpt, str) and wpt.strip().lower() == 'service':
            return 'Préventif'
        try:
            if int(err) > 0:
                return 'Curatif'
        except Exception:
            pass
        return None

    df['Type'] = df.apply(classify, axis=1)

    counts = df['Type'].value_counts().reindex(['Préventif', 'Curatif']).fillna(0)
    total = int(counts.sum())

    # couleurs : Préventif = vert, Curatif = orange
    color_map = {'Préventif': '#4caf50', 'Curatif': '#ff9800'}

    plot_df = pd.DataFrame({'Type': counts.index, 'Count': counts.values})
    fig = px.pie(plot_df, names='Type', values='Count', hole=0.6, color='Type', color_discrete_map=color_map)
    fig.update_traces(textinfo='percent')
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      width=500, height=170,
                      legend=dict(x=0.7, y=0.5, bgcolor='rgba(0,0,0,0)', font=dict(color='white')))

    # annotation centre : mot TOTAL en haut, nombre en dessous
    fig.update_layout(annotations=[dict(text=f"<b>TOTAL</b><br><span style='font-size:18px'>{total}</span>",
                                        x=0.5, y=0.5, showarrow=False, font=dict(color='white'))])

    # Encapsuler le graphique dans un cadre style 'statut systeme'
    plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    html_wrapper = f"""
    <div style="border: 2px solid #00d2b4; padding: 12px; background-color: #1a1c23; width: 700px; height: 190px; border-radius: 4px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0 auto; display: flex; align-items: center;">
        <div style="flex: 1;">
            <div style="color: #9e9e9e; font-size: 12px; font-weight: 600; letter-spacing: 1px; margin-bottom: 6px;">STATUT INTERVENTIONS</div>
            <div style="height:160px">{plot_html}</div>
        </div>
        <div style="flex: 1; padding-left: 20px; color: white; font-size: 14px;">
            <strong>Description :</strong><br>
            Ce graphique en camembert montre la répartition des types d'interventions.<br>
            - <span style="color: #4caf50;">Préventif</span> : Interventions de service planifiées.<br>
            - <span style="color: #ff9800;">Curatif</span> : Interventions suite à une erreur détectée.
        </div>
    </div>
    """

    components.html(html_wrapper, height=300)
