import streamlit as st
from utils.cnx_sql import func_query_sql_df
import pandas as pd 
import altair as alt
from datetime import datetime, timedelta

def func_linechart_taux_performance():

    temps_cycle_theorique = 500 # A definir

    # Periode definir
    dt_fin = datetime.now()
    dt_deb = dt_fin - timedelta(days=90)

    dt_deb_str = dt_deb.strftime('%Y-%m-%d %H:%M:%S')
    dt_fin_str = dt_fin.strftime('%Y-%m-%d %H:%M:%S')

    query_nb_pieces_produites_par_jour = f"""
        SELECT 
            DATE(TimeStamp) as date,
            SUM(CASE WHEN PNo <> 0 THEN 1 ELSE 0 END) as nb_pieces_produites_par_jour
        FROM `tblpartsreport` 
        WHERE TimeStamp BETWEEN '{dt_deb_str}' AND '{dt_fin_str}' 
        GROUP BY DATE(TimeStamp)
    """

    query_temps_fonctionnement_seconds_par_jour = f"""
        SELECT 
            DATE(Start) as date,
            SUM(TIMESTAMPDIFF(SECOND,Start, End)) as temps_fonctionnement_seconds
        FROM `tblfinstep`
        WHERE TimeStamp '{dt_deb_str}' AND '{dt_fin_str}' 
        GROUP BY DATE(Start)
    """

    df_nb_pieces_produites_par_jour = func_query_sql_df(query_nb_pieces_produites_par_jour)
    df_nb_pieces_produites_par_jour['date'] = pd.to_datetime(df_nb_pieces_produites_par_jour['date'])

    df_temps_fonctionnement_seconds_par_jour = func_query_sql_df(query_temps_fonctionnement_seconds_par_jour)
    df_temps_fonctionnement_seconds_par_jour['date'] = pd.to_datetime(df_temps_fonctionnement_seconds_par_jour['date'])

   
    # DataFrame qui contient toutes les jours de la périodes
    df_date = pd.DataFrame({
        'date': pd.date_range(start=dt_deb, end=dt_fin, freq='D', normalize=True)
    })

    # On ramène le nombre de pièces produites pour chaque jour
    df_date_nb_pieces = pd.merge(
        df_date,
        df_nb_pieces_produites_par_jour,
        on = "date",
        how = 'left'
    )

    # On ramène le temps de fonctionnement de chaque jour
    df_date_nb_pieces_temps_fonctionnement = pd.merge(
        df_date_nb_pieces,
        df_temps_fonctionnement_seconds_par_jour,
        on = "date",
        how = "left"
    ).fillna(0)


    df = df_date_nb_pieces_temps_fonctionnement.copy()

    # On calcule de temps de cycle réel
    df['temps_cycle_reel'] = (
        df['nb_pieces_produites_par_jour'].div(
            df['temps_fonctionnement_seconds']
            ).fillna(0)
    )

    # On calcule le taux de performance
    df['taux_performance'] = (
        df['temps_cycle_reel'].div(
            temps_cycle_theorique
            ).fillna(0)
    )

    curve = alt.Chart(df).mark_line(point=True).encode(
        x = alt.X(
            'date:T',
            axis = alt.Axis(
                format = '%d %b',
                title = 'Date',
                titleFontWeight = 'bold',
                # tickMinStep = 86400000 # Force un pas minimum d'un jour (en ms) pour éviter les doublons
                )
        ),
        y = alt.Y(
            'taux_performance:Q',
            axis = alt.Axis(
                title = 'Taux de performance',
                titleFontWeight = 'bold',
                format = '.0%'

                )
            )
    ).properties(
        height=400,
        title = alt.TitleParams(
            text = 'Evolution du Taux de Performance',
            anchor = 'middle',
            fontSize = 30,
            offset=30
        )
    )

    chart = curve

    st.altair_chart(chart, use_container_width=True)