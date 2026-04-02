import streamlit as st
import pandas as pd
from utils.auth import init_users_table
from page_accueil.main_page_accueil import func_page_accueil
from page_404.main_page_404 import func_page_404
from page_production_1.main_page_production_1 import func_page_production_1
from page_production_2.main_page_production_2 import func_page_production_2
from page_logistique_stock.main_page_logistique_stock import func_page_logistique_stock
from page_qualite.main_page_qualite import func_page_qualite
from page_maintenance.main_page_maintenance import func_page_maintenance
from page_admin.main_page_admin import func_page_admin
from page_carte_logistique.main_page_carte_logistique import func_page_carte_logistique
from login_page import login_page

st.set_page_config(layout='wide')

init_users_table()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    login_page()
else:
    # Sidebar : navigation uniquement + lien source de données
    st.sidebar.caption("[🗄️ Source de données](http://localhost:8082)")

    # Construction des pages
    page_accueil    = st.Page(func_page_accueil,          title='Accueil',               icon="🏠")
    page_prod1      = st.Page(func_page_production_1,     title='Page Production 1',     icon="📊")
    page_prod2      = st.Page(func_page_production_2,     title='Page Production 2',     icon="📊")
    page_logistique = st.Page(func_page_logistique_stock, title='Page Logistique/Stock', icon="📦")
    page_qualite    = st.Page(func_page_qualite,          title='Page Qualité',          icon="📈")
    page_maintenance= st.Page(func_page_maintenance,      title='Page Maintenance',      icon="🛠️")
    page_admin      = st.Page(func_page_admin,            title='Administration',        icon="👤")
    page_carte      = st.Page(func_page_carte_logistique, title='Carte Logistique',      icon="🗺️")
    page_404        = st.Page(func_page_404,              title='Page 404',              icon="🚫")

    all_pages = [page_prod1, page_prod2, page_logistique, page_qualite, page_maintenance, page_carte]

    role = st.session_state['role']
    if role == 'admin':
        pages = [page_accueil] + all_pages + [page_admin, page_404]
    elif role == 'maintenance':
        pages = [page_accueil, page_maintenance, page_404]
    elif role == 'production':
        pages = [page_accueil, page_prod1, page_prod2, page_404]
    elif role == 'logistique':
        pages = [page_accueil, page_logistique, page_carte, page_404]
    else:
        pages = [page_accueil, page_404]

    st.session_state["pages_nav"] = {p.title: p for p in pages}
    st.session_state["home_page"] = page_accueil

    app = st.navigation(pages)
    app.run()
