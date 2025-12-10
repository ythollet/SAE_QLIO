import streamlit as st
import mysql.connector
import os # Pour lire les variables d'environnement
import pandas as pd # Importer pandas pour la manipulation des données

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

                # Graphique : Nombre de produits terminés par jour
                df['End'] = pd.to_datetime(df['End'])
                chart_data = df.set_index('End').resample('D').size()
                st.bar_chart(chart_data)
            
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