import streamlit as st
import streamlit.components.v1 as components  # <-- L'arme secrète pour le HTML
import pandas as pd
from utils.cnx_sql import func_query_sql_df

def func_kpi_statut_system():
    # 1. Requête SQL
    query = """
    SELECT 
        CASE 
            WHEN Start IS NOT NULL AND End IS NULL AND Error > 0 THEN 'Erreur'
            WHEN Start IS NOT NULL AND End IS NULL AND Error = 0 THEN 'En marche'
            ELSE 'Attente'
        END AS Statut
    FROM tblorderpos;
    """

    # Récupération du DataFrame
    df_statut_systeme = func_query_sql_df(query)
    
    # 2. Logique pour le statut global
    if df_statut_systeme is None or df_statut_systeme.empty:
        statut_global = 'Attente'
    else:
        statuts = df_statut_systeme['Statut'].unique()
        if 'Erreur' in statuts:
            statut_global = 'Erreur'
        elif 'En marche' in statuts:
            statut_global = 'En marche'
        else:
            statut_global = 'Attente'

    # 3. Paramètres visuels
    if statut_global == 'En marche':
        dot_color = '#4caf50' 
        dot_shadow = 'rgba(76, 175, 80, 0.25)' 
        text_display = 'EN MARCHE'
    elif statut_global == 'Erreur':
        dot_color = '#f44336' 
        dot_shadow = 'rgba(244, 67, 54, 0.25)' 
        text_display = 'ERREUR'
    else:
        dot_color = '#ff9800' 
        dot_shadow = 'rgba(255, 152, 0, 0.25)' 
        text_display = 'ATTENTE'

    # 4. Code HTML complet (j'ai remis la boîte avec la bordure cyan)
    html_kpi = f"""
    <div style="border: 2px solid #00d2b4; padding: 15px 20px; background-color: #1a1c23; width: 250px; border-radius: 4px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <div style="color: #9e9e9e; font-size: 12px; font-weight: 600; letter-spacing: 1px; margin-bottom: 5px;">
            STATUT SYSTÈME
        </div>
        <div style="display: flex; align-items: center;">
            <div style="height: 14px; width: 14px; background-color: {dot_color}; border-radius: 50%; margin-right: 15px; box-shadow: 0 0 0 6px {dot_shadow};">
            </div>
            <div style="color: white; font-size: 24px; font-weight: 800; letter-spacing: 0.5px;">
                {text_display}
            </div>
        </div>
    </div>
    """
    
    # 5. Affichage avec components (Hauteur fixée pour ne pas couper le cadre)
    components.html(html_kpi, height=120)