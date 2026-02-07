import streamlit as st
import pandas as pd 
from page_production_1.main_page_production_1 import func_page_production_1
from page_production_2.main_page_production_2 import func_page_production_2
from page_logistique_stock.main_page_logistique_stock import func_page_logistique_stock

# La configuration de la page doit être la première commande Streamlit
st.set_page_config(layout='wide')

pages = [
    st.Page(func_page_production_1, title = 'Page Production 1', icon = "📊"),
    st.Page(func_page_production_2, title = 'Page Production 2', icon = "📊"),
    st.Page(func_page_logistique_stock, title = 'Page Logistique/Stock')
]

app = st.navigation(pages)

app.run()