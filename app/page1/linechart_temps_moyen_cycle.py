from utils.cnx_sql import func_query_sql_df
import altair as alt
import streamlit as st

def func_linechart_temps_moyen_cycle():

    query = """
        SELECT 
            DATE(Start) as jour,
            CAST(AVG(TIMESTAMPDIFF(MINUTE,Start,End)) as UNSIGNED) as temps_cycle_moyen_minutes
        FROM `tblfinorder` 
        WHERE TIMESTAMPDIFF(DAY,DATE(Start),CURDATE()) <= 100
        GROUP BY DATE(Start)
    """

    df = func_query_sql_df(query)
    
    curve = alt.Chart(df).mark_line(point=True).encode(
        x = alt.X(
            'jour:T',
            axis = alt.Axis(
                format = '%d %b',
                title = 'Date',
                titleFontWeight = 'bold',
                tickMinStep = 86400000 # Force un pas minimum d'un jour (en ms) pour éviter les doublons
                )
        ),
        y = alt.Y(
            'temps_cycle_moyen_minutes:Q',
            axis = alt.Axis(
                title = 'Durée Cycle Moyen (minutes)',
                titleFontWeight = 'bold'
                )
            )
    ).properties(
        title = alt.TitleParams(
            text = 'Temps de Cycle Moyen par Jour',
            anchor = 'middle',
            fontSize = 30
        )
    )

    chart = curve

    st.altair_chart(chart, use_container_width=True)