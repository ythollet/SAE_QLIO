from utils.cnx_sql import func_query_sql_df
import streamlit as st
import altair as alt
import pandas as pd

def func_encours_global():

    limite_pieces_par_buffer = 10

    query_repartition_pieces_buffers = f"""
    SELECT 
        b.Description as nom_buffer,
        COUNT(*) as nb_pieces_buffer,
        CASE WHEN COUNT(*) > {limite_pieces_par_buffer} THEN 'Seuil max dépassé' ELSE 'Seuil max non-dépassé' END as statut
    FROM tblbufferpos as bpos
        INNER JOIN tblbuffer as b
        ON bpos.ResourceId = b.ResourceId AND bpos.BufNo = b.BufNo
    WHERE PNo <> 0
    GROUP BY b.Description
    """

    df = func_query_sql_df(query_repartition_pieces_buffers)


    echelle_couleurs = alt.Scale(
        domain = ['Seuil max', 'Seuil max non-dépassé', 'Seuil max dépassé'],
        range = ["white", "#00811E", "#CD1616"]
    )

    # Barres du graphique
    barres = alt.Chart(df).mark_bar(
        size = 30,
        cornerRadius = 5
        ).encode(
            x = alt.X(
                'nom_buffer:O',
                axis = alt.Axis(
                    title = 'Nom du Buffer',
                    titleFontWeight = 'bold',
                    labelAngle = 0
                    )
                ),
            y = alt.Y(
                'nb_pieces_buffer:Q',
                axis = alt.Axis(
                    title = "Nombre de Pièces",
                    titleFontWeight = 'bold'
                    ),
                ),
            color = alt.Color(
                'statut:N',
                scale = echelle_couleurs
                )
            ).properties(
                height = 400,
                title = alt.TitleParams(
                    text = "Répartition des pièces par buffers",
                    anchor = 'middle',
                    fontSize = 30
                )
            )
    
    # Etiquettes de données
    etiquettes = barres.mark_text(
        dy = -12,
        fontSize = 15,
        color = 'white'
        ).encode(
            text = alt.Text(
                'nb_pieces_buffer:Q'
                )
            )
    
    df_seuil = pd.DataFrame({'label': ['Seuil max'], 'valeur': [limite_pieces_par_buffer]})
    seuil = alt.Chart(df_seuil).mark_rule(strokeDash=[5,5], size=2).encode(
        y='valeur:Q',
        color=alt.Color(
            'label:N', 
            scale=echelle_couleurs, # Associe 'Objectif' à 'red'
            title=""            # Titre de la légende,
            
        )
    )
    
    barchart = barres + etiquettes + seuil

    st.altair_chart(barchart, use_container_width=True)