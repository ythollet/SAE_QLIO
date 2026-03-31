import streamlit as st
import mysql.connector
import pandas as pd
import os

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "client")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "mdp")
DB_NAME = os.environ.get("DB_NAME", "mes4")

def func_get_cnx_sql():
    """
    Crée une connexion à la base de données.
    Reconnecte automatiquement si la connexion a expiré.
    """
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

@st.cache_data(ttl=60)
def func_query_sql_df(in_query: str):
    """
    Exécute une requête SQL et retourne un DataFrame pandas.
    Crée une nouvelle connexion à chaque appel (évite les connexions expirées).
    """
    conn = func_get_cnx_sql()
    try:
        return pd.read_sql(in_query, conn)
    finally:
        conn.close()
