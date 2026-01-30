import streamlit as st
from utils.cnx_sql import func_query_sql_df
import pandas as pd 
from datetime import datetime
from dateutil.relativedelta import relativedelta
import altair as alt

def func_barchart_nb_produits_termines_par_jour():


    seuil_objectif_graphique = 4

    query = f"""
        SELECT 
            DATE(End) as jour,
            COUNT(ONo) as nb_produits_termines,
            CASE 
                WHEN COUNT(ONo) > {seuil_objectif_graphique} THEN 'Objectif atteint'
                ELSE 'Objectif non-atteint'
            END
            as statut
        FROM tblfinorder
        WHERE End > (CURDATE() - INTERVAL 100 DAY)
        GROUP BY DATE(End) 
        """
    
    df = func_query_sql_df(
        in_query = query
    )              
    
    # Barres du graphique
    barres = alt.Chart(df).mark_bar(
        size = 30,
        cornerRadius = 5
        ).encode(
                x = alt.X(
                    'jour:T',
                    axis = alt.Axis(
                        format = '%d %b',
                        title = 'Date',
                        titleFontWeight = 'bold',
                        # tickMinStep = 86400000 # Force un pas minimum d'un jour (en ms) pour éviter les doublons
                        )
                    ),
                y = alt.Y(
                    'nb_produits_termines:Q',
                    axis = alt.Axis(
                        title = 'Nombre Produits Terminés',
                        titleFontWeight = 'bold'
                        )
                    ),
                color = alt.Color(
                    'statut:N',
                    scale = alt.Scale(
                        domain = ['Objectif atteint', 'Objectif non-atteint'],
                        range = ["#00811E", "#CD1616"]
                ),
            )                      
                ).properties(
                    height = 400,
                    title = alt.TitleParams(
                        text = 'Nombre de Produits Terminés par Jour',
                        anchor = 'middle',
                        fontSize = 30
                    )
                    
                )

    # Etiquettes de données
    etiquettes = barres.mark_text(
        dy = -12,
        fontSize = 15
        ).encode(
            text = alt.Text(
                'nb_produits_termines:Q', 
                format = '.0f',
                
                )
            )

    # Seuil objectif
    df_seuil = pd.DataFrame({'seuil': [4]})
    seuil = alt.Chart(df_seuil).mark_rule(
        color = 'white',
        strokeDash = [5, 8],
        strokeCap = 'round'
        ).encode(
            y = 'seuil'
        )

    barchart = barres + etiquettes + seuil

    st.altair_chart(barchart, use_container_width=True)