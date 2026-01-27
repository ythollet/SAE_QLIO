import streamlit as st
import mysql.connector
import pandas as pd
import os

# Récupération des informations de connexion depuis les variables d'environnement
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "client")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "mdp")
DB_NAME = os.environ.get("DB_NAME", "mes4")

@st.cache_resource
def func_get_cnx_sql():
    """
    Crée une connexion à la base de données et la met en cache.
    Streamlit gère la persistance de l'objet connexion pour éviter de se reconnecter à chaque interaction.
    """
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@st.cache_data(ttl=60) # Optionnel : met en cache les données 60 secondes
def func_query_sql_df(in_query: str):
    """
    Exécute une requête SQL et retourne un DataFrame pandas en utilisant la connexion partagée.
    """
    conn = func_get_cnx_sql()
    return pd.read_sql(in_query, conn)
    
