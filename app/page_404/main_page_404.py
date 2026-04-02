import streamlit as st
from utils.top_banner import func_top_banner


def func_page_404():
    func_top_banner(key="p404", show_date_filter=False)

    st.markdown("""
        <style>
        .bloc-404 {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 60vh;
            text-align: center;
        }
        .chiffre-404 {
            font-size: 160px;
            font-weight: 900;
            color: #1de9b6;
            line-height: 1;
            margin-bottom: 10px;
        }
        .titre-404 {
            font-size: 28px;
            font-weight: 800;
            color: white;
            letter-spacing: 4px;
            margin-bottom: 16px;
        }
        .sous-titre-404 {
            font-size: 16px;
            color: #9e9e9e;
            margin-bottom: 40px;
        }
        </style>

        <div class="bloc-404">
            <div class="chiffre-404">404</div>
            <div class="titre-404">PAGE INTROUVABLE</div>
            <div class="sous-titre-404">La page que vous recherchez n'est pas disponible ou a été déplacée.</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("RETOUR ACCUEIL", use_container_width=True, type="primary"):
            home = st.session_state.get("home_page")
            if home is not None:
                st.switch_page(home)
