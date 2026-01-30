from utils.cnx_sql import func_query_sql_df
import altair as alt
import streamlit as st

def func_linechart_temps_moyen_cycle():

    query = """
        SELECT 
            Start as "date",
            CAST(TIMESTAMPDIFF(MINUTE,Start,End) as UNSIGNED) as temps_cycle_minutes
        FROM `tblfinorder` 
        WHERE TIMESTAMPDIFF(DAY,DATE(Start),CURDATE()) <= 100
    """

    df = func_query_sql_df(query)
    
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
            'temps_cycle_minutes:Q',
            axis = alt.Axis(
                title = 'Durée des Cycles de Frabrication (minutes)',
                titleFontWeight = 'bold'
                )
            )
    ).properties(
        height=400,
        title = alt.TitleParams(
            text = 'Evolution du Temps de Cycle',
            anchor = 'middle',
            fontSize = 30,
            offset=30
        )
    )

    chart = curve

    st.altair_chart(chart, use_container_width=True)