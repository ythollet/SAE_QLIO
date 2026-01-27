import streamlit as st
import mysql.connector
import os # Pour lire les variables d'environnement
import pandas as pd # Importer pandas pour la manipulation des données
from datetime import datetime
from dateutil.relativedelta import relativedelta
import altair as alt


# La configuration de la page doit être la première commande Streamlit
st.set_page_config(layout='wide')

# Récupération des informations de connexion depuis les variables d'environnement
DB_HOST = os.environ.get("DB_HOST", "db") # Le nom de service est 'db'
DB_USER = os.environ.get("DB_USER", "client")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "mdp")
DB_NAME = os.environ.get("DB_NAME", "mes4")


@st.cache_resource # Mise en cache de la connexion
def func_get_cnx_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

conn = func_get_cnx_db()

@st.cache_data
def func_query_db(
    in_query: str,
):
    return pd.read_sql(in_query, conn)


def func_page1():
    try:
        st.header("Affichage des 100 premières lignes")

        query = "SELECT * FROM tblfinorder;"
        df = func_query_db(
            in_query = query
        )

        st.dataframe(df)

        st.markdown("""
            <style>
            div[data-testid="stMetric"] {
                display: flex; 
                flex-direction: column;
                align-items: center; 
                text-align: center; 
            }

            div[data-testid="stMetricLabel"] {
                text-align: center; 
                width: 100%; 
            }
            </style>
        """, 
        unsafe_allow_html = True
        )

        with st.container(border = True): 

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    label = "nb produis terminés", 
                    value = df['End'].count()
                )

                def func_barchart_end_products_by_days(in_df):
                    
                    # On travaille sur une copie pour éviter de modifier le DF original
                    in_df = in_df.copy()


                    # Graphique : Nombre de produits terminés par jour
                    in_df['End'] = pd.to_datetime(in_df['End'])
                    
                    # On récupère la date actuelle
                    today = datetime.now()

                    # On récupère les 60 derniers jours
                    mask = (in_df['End'] > today-relativedelta(days = 100))
                    col_end = in_df['End'].loc[mask].reset_index(drop=True)

                    # On groupe par jour et on coumpte les produits terminés pour chaque jour
                    df_end_groupby_day = col_end.groupby(col_end.dt.date).count().rename("nb_produits_termines").to_frame().reset_index()

                    # Barres du graphique
                    barres = alt.Chart(df_end_groupby_day).mark_bar(
                        size = 30,
                        cornerRadius = 5
                        ).encode(
                            x = alt.X(
                                'End:T',
                                axis = alt.Axis(
                                    format = '%d %b',
                                    title = 'Date',
                                    titleFontWeight = 'bold'
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
                                'nb_produits_termines:Q',
                                scale = alt.Scale(
                                    range = ["#D0A0F7", "#9139D8", "#7A06DA"]
                            ),
                            legend = None
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

                func_barchart_end_products_by_days(df)
            
            with col2:

                st.metric(
                    label = "temps moyen traitement", 
                    value = str((df['End']-df['Start']).mean()).split('.')[0].replace('0 days ','')
                )

    except mysql.connector.Error as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue : {e}")


pages = [
    st.Page(func_page1, title = 'Page 1', icon = "📊")
]

app = st.navigation(pages)

app.run()