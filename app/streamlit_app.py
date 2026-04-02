import streamlit as st
import pandas as pd
from page_production_1.main_page_production_1 import func_page_production_1
from page_production_2.main_page_production_2 import func_page_production_2
from page_logistique_stock.main_page_logistique_stock import func_page_logistique_stock
from page_qualite.main_page_qualite import func_page_qualite
from page_maintenance.main_page_maintenance import func_page_maintenance
from page_admin.main_page_admin import func_page_admin
from login_page import login_page

# La configuration de la page doit être la première commande Streamlit
st.set_page_config(layout='wide')

# Vérifier l'authentification
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    login_page()
else:
    # Afficher le rôle dans la sidebar
    st.sidebar.write(f"Connecté en tant que: {st.session_state['username']} ({st.session_state['role']})")
    if st.sidebar.button("Se déconnecter"):
        st.session_state['authenticated'] = False
        st.rerun()

    # Définir les pages autorisées par rôle
    all_pages = [
        st.Page(func_page_production_1, title='Page Production 1', icon="📊"),
        st.Page(func_page_production_2, title='Page Production 2', icon="📊"),
        st.Page(func_page_logistique_stock, title='Page Logistique/Stock'),
        st.Page(func_page_qualite, title='Page Qualité', icon="📈"),
        st.Page(func_page_maintenance, title='Page Maintenance', icon="🛠️")
    ]
    
    admin_page = st.Page(func_page_admin, title='Administration', icon="👤")

    role = st.session_state['role']
    if role == 'admin':
        pages = all_pages + [admin_page]
    elif role == 'maintenance':
        pages = [p for p in all_pages if 'Maintenance' in p.title]
    elif role == 'production':
        pages = [p for p in all_pages if 'Production' in p.title]
    elif role == 'logistique':
        pages = [p for p in all_pages if 'Logistique' in p.title]
    else:
        pages = []  # Aucun accès si rôle inconnu

    app = st.navigation(pages)
    app.run()