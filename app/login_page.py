import streamlit as st
from utils.auth import authenticate_user

def login_page():
    # CSS pour styliser la page
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
    }
    .login-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.9);
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        color: #333;
        margin-bottom: 1rem;
    }
    .stTextInput > div > div > input:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.5);
    }
    .login-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 18px;
        font-weight: bold;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    .login-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .error-message {
        background-color: rgba(255, 87, 87, 0.8);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .success-message {
        background-color: rgba(72, 187, 120, 0.8);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-top: 1rem;
    }
    body {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    # Conteneur principal
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">🔐 Connexion Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2rem; margin-bottom: 2rem;">Téléphon</p>', unsafe_allow_html=True)

    username = st.text_input("👤 Nom d'utilisateur").strip()
    password = st.text_input("🔒 Mot de passe", type="password").strip()

    if st.button("Se connecter", key="login_button"):
        if username and password:
            role = authenticate_user(username, password)
            if role:
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['role'] = role
                st.markdown('<div class="success-message">✅ Connexion réussie !</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown('<div class="error-message">❌ Nom d\'utilisateur ou mot de passe incorrect</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠️ Veuillez saisir un nom d\'utilisateur et un mot de passe</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)