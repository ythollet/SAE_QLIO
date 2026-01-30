import streamlit as st
import pandas as pd 
from page_production_1.main_page_production_1 import *
from utils.cnx_sql import func_query_sql_df

# La configuration de la page doit être la première commande Streamlit
st.set_page_config(layout='wide')

pages = [
    st.Page(func_page_production_1, title = 'Page Production 1', icon = "📊")
]

app = st.navigation(pages)

app.run()