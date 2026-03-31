import streamlit as st
import altair as alt
import pandas as pd
from utils.cnx_sql import func_query_sql_df

def func_linechart_taux_fonctionnement(temps_planifie_h: int):

    temps_planifie_s = temps_planifie_h * 3600
    cible = 90  # % cible quotidienne

    # tblmachinereport(AutomaticMode, Busy, ErrorL0/L1/L2, TimeStamp)
    # Taux de fonctionnement par jour = temps fonctionnel / temps planifié
    df = func_query_sql_df(f"""
        WITH etats AS (
            SELECT
                DATE(TimeStamp) AS jour,
                TimeStamp,
                AutomaticMode, Busy, ErrorL0, ErrorL1, ErrorL2,
                LEAD(TimeStamp) OVER (PARTITION BY ResourceID ORDER BY TimeStamp) AS next_ts
            FROM tblmachinereport
        )
        SELECT
            jour,
            ROUND(
                LEAST(
                    SUM(CASE
                        WHEN AutomaticMode = 1 AND Busy = 1
                             AND ErrorL0 = 0 AND ErrorL1 = 0 AND ErrorL2 = 0
                        THEN TIMESTAMPDIFF(SECOND, TimeStamp, next_ts)
                        ELSE 0
                    END) / {temps_planifie_s} * 100,
                    100
                ),
            1) AS taux_fonctionnement
        FROM etats
        WHERE next_ts IS NOT NULL
        GROUP BY jour
        ORDER BY jour
    """)

    if df.empty:
        st.info("Pas de données disponibles.")
        return

    df['jour'] = pd.to_datetime(df['jour'])

    courbe = alt.Chart(df).mark_line(
        point=alt.OverlayMarkDef(color='#1de9b6', size=60),
        color='#1de9b6'
    ).encode(
        x=alt.X('jour:T', axis=alt.Axis(title='DATE', titleFontWeight='bold', format='%Y-%m-%d')),
        y=alt.Y(
            'taux_fonctionnement:Q',
            scale=alt.Scale(domain=[0, 100]),
            axis=alt.Axis(title='TAUX DE FONCTIONNEMENT (EN %)', titleFontWeight='bold')
        )
    ).properties(
        height=350,
        title=alt.TitleParams(
            text='EVOLUTION DU TAUX DE FONCTIONNEMENT (TEMPS DE FONCTIONNEMENT / TEMPS PLANIFIÉ)',
            anchor='middle',
            fontSize=13,
            fontWeight='bold'
        )
    )

    df_cible = pd.DataFrame({'cible': [cible]})
    ligne_cible = alt.Chart(df_cible).mark_rule(
        color='red', strokeDash=[6, 4]
    ).encode(y='cible:Q')

    texte_cible = alt.Chart(df_cible).mark_text(
        align='right', dx=-4, dy=-6, color='red', fontSize=11
    ).encode(
        y='cible:Q',
        x=alt.value(700),
        text=alt.value(f'CIBLE QUOTIDIENNE ({cible}%)')
    )

    # Zone critique sous la cible
    zone_critique = alt.Chart(pd.DataFrame({'y1': [0], 'y2': [cible - 10]})).mark_rect(
        opacity=0.15, color='red'
    ).encode(
        y='y1:Q',
        y2='y2:Q'
    )

    st.altair_chart(zone_critique + courbe + ligne_cible + texte_cible, use_container_width=True)
