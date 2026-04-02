import streamlit as st
from datetime import date


def func_top_banner(key: str = "banner", show_date_filter: bool = True):
    """
    Bandeau haut : filtre de période (gauche) + bouton déconnexion (droite).
    Retourne (date_debut, date_fin) ou (None, None) si show_date_filter=False.
    """
    col_label, col_deb, col_fin, col_user, col_logout = st.columns([1, 2, 2, 2, 1])

    with col_label:
        st.markdown("<p style='margin:0; color:#9e9e9e; font-size:12px; padding-top:8px;'>PLAGE DE TEMPS</p>",
                    unsafe_allow_html=True)

    if show_date_filter:
        with col_deb:
            date_debut = st.date_input("Date de début", value=date(2023, 1, 1), key=f"{key}_debut",
                                       label_visibility="collapsed")
        with col_fin:
            date_fin = st.date_input("Date de fin", value=date.today(), key=f"{key}_fin",
                                     label_visibility="collapsed")
    else:
        date_debut, date_fin = None, None
        col_deb.empty()
        col_fin.empty()

    with col_user:
        user = st.session_state.get("username", "")
        role = st.session_state.get("role", "")
        st.markdown(
            f"<p style='margin:0; color:white; text-align:right; padding-top:8px;'>👤 {user} <span style='color:#9e9e9e'>({role})</span></p>",
            unsafe_allow_html=True
        )

    with col_logout:
        if st.button("⏻", key=f"{key}_logout", use_container_width=True, help="Se déconnecter"):
            st.session_state['authenticated'] = False
            st.rerun()

    if show_date_filter and date_debut > date_fin:
        st.error("La date de début doit être antérieure à la date de fin.")
        return None, None

    return date_debut, date_fin
