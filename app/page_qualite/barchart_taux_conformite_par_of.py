import streamlit as st
import altair as alt
import pandas as pd
from utils.cnx_sql import func_query_sql_df

def func_barchart_taux_conformite_par_of():
    query = """
        SELECT
            f.ONo,
            SUM(CASE WHEN p.ErrorID = 0 THEN 1 ELSE 0 END) AS nb_ok,
            SUM(CASE WHEN p.ErrorID != 0 THEN 1 ELSE 0 END) AS nb_nok,
            COUNT(p.PNo) AS nb_total,
            ROUND(
                SUM(CASE WHEN p.ErrorID = 0 THEN 1 ELSE 0 END) / COUNT(p.PNo) * 100,
                0
            ) AS taux_conformite
        FROM tblpartsreport p
        JOIN (
            SELECT DISTINCT PNo, ONo
            FROM tblfinorderpos
            WHERE PNo != 0
        ) f ON p.PNo = f.PNo
        GROUP BY f.ONo
        ORDER BY f.ONo
    """
    df = func_query_sql_df(query)

    if df.empty:
        st.info("Aucune donnée de production disponible.")
        return

    df['ONo'] = 'OF-' + df['ONo'].astype(str)

    # Reshape en format long pour stacked bar
    df_long = pd.melt(
        df,
        id_vars=['ONo', 'nb_total', 'taux_conformite'],
        value_vars=['nb_ok', 'nb_nok'],
        var_name='type',
        value_name='nb_pieces'
    )
    df_long['type'] = df_long['type'].map({'nb_ok': 'Pièces OK', 'nb_nok': 'Pièces NOK'})

    barres = alt.Chart(df_long).mark_bar().encode(
        x=alt.X(
            'ONo:N',
            axis=alt.Axis(title='ORDRE DE FABRICATION (ONo)', titleFontWeight='bold', labelAngle=0)
        ),
        y=alt.Y(
            'nb_pieces:Q',
            axis=alt.Axis(title='NOMBRE DE PIÈCES', titleFontWeight='bold')
        ),
        color=alt.Color(
            'type:N',
            scale=alt.Scale(
                domain=['Pièces OK', 'Pièces NOK'],
                range=['#1de9b6', '#e05252']
            ),
            legend=alt.Legend(title=None)
        ),
        order=alt.Order('type:N', sort='descending')
    ).properties(
        height=400,
        title=alt.TitleParams(
            text='RÉPARTITION OK/NOK PAR ORDRE DE FABRICATION (OF)',
            anchor='middle',
            fontSize=14,
            fontWeight='bold'
        )
    )

    # Étiquettes de pourcentage au dessus de chaque barre
    df_total = df[['ONo', 'nb_total', 'taux_conformite']].copy()
    etiquettes = alt.Chart(df_total).mark_text(
        dy=-10,
        fontSize=13,
        fontWeight='bold',
        color='white'
    ).encode(
        x=alt.X('ONo:N'),
        y=alt.Y('nb_total:Q'),
        text=alt.Text('taux_conformite:Q', format='.0f', formatType='number')
    ).transform_calculate(
        label="datum.taux_conformite + '%'"
    ).encode(text='label:N')

    st.altair_chart(barres + etiquettes, use_container_width=True)
