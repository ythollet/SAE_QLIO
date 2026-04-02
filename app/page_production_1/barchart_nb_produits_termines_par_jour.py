import streamlit as st
from utils.cnx_sql import func_query_sql_df
import pandas as pd
import altair as alt

def func_barchart_nb_produits_termines_par_jour(date_debut=None, date_fin=None):

    seuil_objectif_graphique = 4

    filtre = (
        f"WHERE DATE(End) BETWEEN '{date_debut}' AND '{date_fin}'"
        if date_debut
        else "WHERE End > (CURDATE() - INTERVAL 90 DAY)"
    )

    query = f"""
        SELECT
            DATE(End) as jour,
            COUNT(ONo) as nb_produits_termines,
            CASE
                WHEN COUNT(ONo) > {seuil_objectif_graphique} THEN 'Objectif atteint'
                ELSE 'Objectif non-atteint'
            END as statut
        FROM tblfinorder
        {filtre}
        GROUP BY DATE(End)
        ORDER BY jour
    """

    df = func_query_sql_df(in_query=query)

    if df.empty:
        st.info("Aucune donnée sur cette période.")
        return

    df['jour'] = pd.to_datetime(df['jour'])
    nb_barres = len(df)

    # Largeur des barres adaptée au nombre de points
    if nb_barres <= 5:
        bar_size = 60
    elif nb_barres <= 15:
        bar_size = 40
    elif nb_barres <= 40:
        bar_size = 20
    else:
        bar_size = max(4, int(700 / nb_barres))

    # Format de date adapté
    if nb_barres <= 15:
        date_format = '%d %b %Y'
    elif nb_barres <= 60:
        date_format = '%d %b'
    else:
        date_format = '%b %Y'

    barres = alt.Chart(df).mark_bar(
        size=bar_size,
        cornerRadius=3
    ).encode(
        x=alt.X(
            'jour:T',
            axis=alt.Axis(
                format=date_format,
                title='Date',
                titleFontWeight='bold',
                labelAngle=-30,
                tickMinStep=86400000
            )
        ),
        y=alt.Y(
            'nb_produits_termines:Q',
            axis=alt.Axis(
                title='Nombre Produits Terminés',
                titleFontWeight='bold'
            )
        ),
        color=alt.Color(
            'statut:N',
            scale=alt.Scale(
                domain=['Objectif atteint', 'Objectif non-atteint'],
                range=['#1de9b6', '#CD1616']
            ),
            legend=alt.Legend(title=None)
        ),
        tooltip=[
            alt.Tooltip('jour:T', title='Date', format='%d/%m/%Y'),
            alt.Tooltip('nb_produits_termines:Q', title='Produits terminés'),
            alt.Tooltip('statut:N', title='Statut')
        ]
    ).properties(
        height=350,
        title=alt.TitleParams(
            text='NOMBRE DE PRODUITS TERMINÉS PAR JOUR',
            anchor='middle',
            fontSize=13,
            fontWeight='bold'
        )
    )

    etiquettes = barres.mark_text(
        dy=-10,
        fontSize=12 if nb_barres <= 20 else 0  # masque les labels si trop serré
    ).encode(
        text=alt.Text('nb_produits_termines:Q', format='.0f')
    )

    df_seuil = pd.DataFrame({'seuil': [seuil_objectif_graphique]})
    seuil = alt.Chart(df_seuil).mark_rule(
        color='white',
        strokeDash=[5, 8],
        strokeCap='round'
    ).encode(y='seuil:Q')

    st.altair_chart(barres + etiquettes + seuil, use_container_width=True)
