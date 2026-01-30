import streamlit as st
import altair as alt
import pandas as pd
from utils.cnx_sql import func_query_sql_df

def func_taux_occupation_buffers():

    objectif_taux_occ_buffers = 0.8

    query = f"""
        SELECT
            BufNo,
            SUM(CASE WHEN PNo <> 0 THEN 1 ELSE 0 END) / COUNT(*) as taux_occupation_buffer,
            (CASE 
                WHEN SUM(CASE WHEN PNo <> 0 THEN 1 ELSE 0 END) / COUNT(*) > {objectif_taux_occ_buffers} THEN 'Objectif atteint' 
                ELSE 'Objectif non-atteint'
                END) as statut
        FROM tblbufferpos
        GROUP BY BufNo
    """

    df = func_query_sql_df(query)

    echelle_couleurs = alt.Scale(
        domain=['Objectif', 'Objectif atteint', 'Objectif non-atteint'],
        range=["white", "#00811E", "#CD1616"]
    )

    # Barres du graphique
    barres = alt.Chart(df).mark_bar(
        size = 30,
        cornerRadius = 5
        ).encode(
            x = alt.X(
                'BufNo:O',
                axis = alt.Axis(
                    title = 'Numéro du Buffer',
                    titleFontWeight = 'bold',
                    labelAngle = 0
                    
                    )
                ),
            y = alt.Y(
                'taux_occupation_buffer:Q',
                axis = alt.Axis(
                    title = "Taux d'occupation",
                    titleFontWeight = 'bold',
                    format = '.0%'
                    ),
                scale = alt.Scale(domain=[0,1])
                ),
            color = alt.Color(
                'statut:N',
                scale = echelle_couleurs
                )
            ).properties(
                height = 400,
                title = alt.TitleParams(
                    text = "Taux d'occupation des buffers",
                    anchor = 'middle',
                    fontSize = 30
                )
            )
    
    # Etiquettes de données
    etiquettes = barres.mark_text(
        dy = -12,
        fontSize = 15,
        color = 'white'
        ).encode(
            text = alt.Text(
                'taux_occupation_buffer:Q', 
                format = '.0%'
                )
            )
    
    df_seuil = pd.DataFrame({'label': ['Objectif'], 'valeur': [0.8]})
    seuil = alt.Chart(df_seuil).mark_rule(strokeDash=[5,5], size=2).encode(
        y='valeur:Q',
        color=alt.Color(
            'label:N', 
            scale=echelle_couleurs, # Associe 'Objectif' à 'red'
            title=""            # Titre de la légende,
            
        )
    )
    
    barchart = barres + etiquettes + seuil

    st.altair_chart(barchart, use_container_width=True)