import streamlit as st
import bcrypt
from utils.cnx_sql import func_get_cnx_sql


def func_page_admin():
    st.title("Administration")
    st.write("Page d'administration - accès réservé aux administrateurs")

    st.header("Créer un nouvel utilisateur")

    with st.form("create_user_form"):
        username = st.text_input("Nom d'utilisateur").strip()
        password = st.text_input("Mot de passe", type="password").strip()
        role = st.selectbox("Rôle", ["admin", "maintenance", "production", "logistique"])
        submitted = st.form_submit_button("Créer l'utilisateur")

        if submitted:
            if not username or not password:
                st.error("Veuillez remplir tous les champs.")
            else:
                try:
                    conn = func_get_cnx_sql()
                    cursor = conn.cursor()

                    # Hacher le mot de passe
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    # Insérer l'utilisateur
                    cursor.execute(
                        "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                        (username, password_hash, role)
                    )
                    conn.commit()

                    st.success(f"Utilisateur '{username}' créé avec succès avec le rôle '{role}'.")

                except Exception as e:
                    if "Duplicate entry" in str(e) or "1062" in str(e):
                        st.error("Le nom d'utilisateur existe déjà.")
                    else:
                        st.error(f"Erreur lors de la création de l'utilisateur: {e}")
                finally:
                    if 'cursor' in locals():
                        cursor.close()
                    if 'conn' in locals():
                        conn.close()
