import streamlit as st
import altair as alt
import pandas as pd
from utils.cnx_sql import func_query_sql_df

def func_barchart_top5_causes_nok(date_debut=None, date_fin=None):
    filtre = (
        f"AND DATE(p.TimeStamp) BETWEEN '{date_debut}' AND '{date_fin}'"
        if date_debut
        else ""
    )
    query = f"""
        SELECT
            COALESCE(e.Description, CONCAT('Erreur ', p.ErrorID)) AS cause,
            COUNT(p.ErrorID) AS nb_erreurs
        FROM tblpartsreport p
        LEFT JOIN tblerrorcodes e ON p.ErrorID = e.ErrorID
        WHERE p.ErrorID != 0
        {filtre}
        GROUP BY p.ErrorID, e.Description
        ORDER BY nb_erreurs DESC
        LIMIT 5
    """
    df = func_query_sql_df(query)

    if df.empty:
        st.info("Aucune pièce NOK détectée.")
        return

    df = df.sort_values('nb_erreurs', ascending=False).reset_index(drop=True)
    df['cumul_pct'] = df['nb_erreurs'].cumsum() / df['nb_erreurs'].sum() * 100

    barres = alt.Chart(df).mark_bar(color='#555555').encode(
        x=alt.X(
            'cause:N',
            sort=alt.SortField('nb_erreurs', order='descending'),
            axis=alt.Axis(title='CAUSE D\'ERREUR', titleFontWeight='bold', labelAngle=-20)
        ),
        y=alt.Y(
            'nb_erreurs:Q',
            axis=alt.Axis(title='NOMBRE D\'OCCURRENCE', titleFontWeight='bold')
        )
    )

    etiquettes = barres.mark_text(
        dy=-10,
        fontSize=13,
        fontWeight='bold',
        color='white'
    ).encode(
        text=alt.Text('nb_erreurs:Q', format='.0f')
    )

    courbe = alt.Chart(df).mark_line(
        color='red',
        point=alt.OverlayMarkDef(color='red', size=60)
    ).encode(
        x=alt.X(
            'cause:N',
            sort=alt.SortField('nb_erreurs', order='descending')
        ),
        y=alt.Y(
            'cumul_pct:Q',
            axis=alt.Axis(title='% CUMULÉ', titleFontWeight='bold'),
            scale=alt.Scale(domain=[0, 100])
        )
    )

    chart = alt.layer(barres + etiquettes, courbe).resolve_scale(
        y='independent'
    ).properties(
        height=400,
        title=alt.TitleParams(
            text='DIAGRAMME DE PARETO DES CAUSES PRINCIPALES D\'ERREUR',
            anchor='middle',
            fontSize=14,
            fontWeight='bold'
        )
    )

    st.altair_chart(chart, use_container_width=True)
