import streamlit as st
import altair as alt
import pandas as pd
from utils.cnx_sql import func_query_sql_df


def func_linechart_temps_cycle(date_debut=None, date_fin=None):

    cible_min = 10  # minutes

    filtre = (
        f"WHERE DATE(End) BETWEEN '{date_debut}' AND '{date_fin}'"
        if date_debut
        else ""
    )

    query = f"""
        SELECT
            ONo,
            DATE(End) AS jour,
            ROUND(TIMESTAMPDIFF(SECOND, Start, End) / 60.0, 2) AS temps_cycle_min
        FROM tblfinorder
        WHERE Start IS NOT NULL AND End IS NOT NULL
        {("AND DATE(End) BETWEEN '" + str(date_debut) + "' AND '" + str(date_fin) + "'") if date_debut else ""}
        ORDER BY End
    """

    df = func_query_sql_df(query)

    if df.empty:
        st.info("Aucune donnée sur cette période.")
        return

    df['ONo'] = df['ONo'].astype(str)
    df['en_retard'] = df['temps_cycle_min'] > cible_min

    courbe = alt.Chart(df).mark_line(
        point=alt.OverlayMarkDef(size=60),
        color='#1de9b6'
    ).encode(
        x=alt.X(
            'jour:T',
            axis=alt.Axis(title='DATE DE FIN D\'ORDRE', titleFontWeight='bold', format='%Y-%m-%d')
        ),
        y=alt.Y(
            'temps_cycle_min:Q',
            axis=alt.Axis(title='TEMPS DE CYCLE (MINUTES)', titleFontWeight='bold')
        ),
        tooltip=[
            alt.Tooltip('ONo:N', title='Ordre'),
            alt.Tooltip('temps_cycle_min:Q', title='Temps cycle (min)', format='.1f'),
            alt.Tooltip('jour:T', title='Date', format='%Y-%m-%d')
        ]
    )

    df_cible = pd.DataFrame({'cible': [cible_min]})
    ligne_cible = alt.Chart(df_cible).mark_rule(
        color='red', strokeDash=[6, 4]
    ).encode(y='cible:Q')

    texte_cible = alt.Chart(df_cible).mark_text(
        align='right', dx=-4, dy=-8, color='red', fontSize=11
    ).encode(
        y='cible:Q',
        x=alt.value(700),
        text=alt.value(f'CIBLE ({cible_min} MIN)')
    )

    # Zone rouge au-dessus de la cible
    df_zone = pd.DataFrame({'y1': [cible_min], 'y2': [df['temps_cycle_min'].max() * 1.1]})
    zone_retard = alt.Chart(df_zone).mark_rect(
        opacity=0.12, color='red'
    ).encode(
        y='y1:Q',
        y2='y2:Q'
    )

    chart = alt.layer(zone_retard, courbe, ligne_cible, texte_cible).properties(
        height=400,
        title=alt.TitleParams(
            text='EVOLUTION DU TEMPS DE CYCLE (END - START) PAR ORDRE',
            anchor='middle',
            fontSize=13,
            fontWeight='bold'
        )
    )

    st.altair_chart(chart, use_container_width=True)
