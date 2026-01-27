import streamlit as st
import pandas as pd 
from datetime import datetime
from dateutil.relativedelta import relativedelta
import altair as alt
from page1.barchart_end_products_by_days import *

def func_barchart_end_products_by_days(in_df_tblfinorder):
                    
    # On travaille sur une copie pour éviter de modifier le DF original
    in_df_tblfinorder = in_df_tblfinorder.copy()

    # Graphique : Nombre de produits terminés par jour
    in_df_tblfinorder['End'] = pd.to_datetime(in_df_tblfinorder['End'])
    
    # On récupère la date actuelle
    today = datetime.now()

    # On récupère les 60 derniers jours
    mask = (in_df_tblfinorder['End'] > today-relativedelta(days = 100))
    col_end = in_df_tblfinorder['End'].loc[mask].reset_index(drop=True)

    # On groupe par jour et on coumpte les produits terminés pour chaque jour
    df_end_groupby_day = col_end.groupby(col_end.dt.date).count().rename("nb_produits_termines").to_frame().reset_index()
    
    # Barres du graphique
    barres = alt.Chart(df_end_groupby_day).mark_bar(
        size = 30,
        cornerRadius = 5
        ).transform_calculate(
            statut = "datum.nb_produits_termines > 4? 'Objectif atteint' : 'Objectif non-atteint'"
            ).encode(
                x = alt.X(
                    'End:T',
                    axis = alt.Axis(
                        format = '%d %b',
                        title = 'Date',
                        titleFontWeight = 'bold',
                        tickMinStep = 86400000 # Force un pas minimum d'un jour (en ms) pour éviter les doublons
                        )
                    ),
                y = alt.Y(
                    'nb_produits_termines',
                    axis = alt.Axis(
                        title = 'Nombre produits terminés',
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
                    title = alt.TitleParams(
                        text = 'Nombre de produits terminés par jour',
                        anchor = 'middle',
                        fontSize = 30
                    )
                    
                )

    # Etiquettes de données
    etiquettes = barres.mark_text(
        # color = 'white',
        dy = -12,
        fontSize = 15
        ).encode(
            text = alt.Text(
                'nb_produits_termines', 
                format = '.0f',
                
                )
            )

    # Seuil objectif
    df_seuil = pd.DataFrame({'seuil': [4]})
    seuil = alt.Chart(df_seuil).mark_rule(
        color = 'chartreuse',
        strokeDash = [5, 8],
        strokeCap = 'round'
        ).encode(
            y = 'seuil'
        )

    barchart = barres + etiquettes + seuil

    st.altair_chart(barchart, use_container_width=True)