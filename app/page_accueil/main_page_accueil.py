import streamlit as st


MODULES = [
    {
        "key": "production_1",
        "initiale": "P1",
        "titre": "PRODUCTION 1",
        "description": "Ligne d'assemblage principale",
        "page_title": "Page Production 1",
    },
    {
        "key": "production_2",
        "initiale": "P2",
        "titre": "PRODUCTION 2",
        "description": "Ligne robotisée secondaire",
        "page_title": "Page Production 2",
    },
    {
        "key": "logistique",
        "initiale": "L",
        "titre": "LOGISTIQUE",
        "description": "Gestion des stocks et buffers",
        "page_title": "Page Logistique/Stock",
    },
    {
        "key": "qualite",
        "initiale": "Q",
        "titre": "QUALITÉ",
        "description": "Suivi rebuts et conformité",
        "page_title": "Page Qualité",
    },
    {
        "key": "maintenance",
        "initiale": "M",
        "titre": "MAINTENANCE",
        "description": "État machines et interventions",
        "page_title": "Page Maintenance",
    },
]


def func_page_accueil():
    st.markdown("""
        <style>
        .accueil-titre {
            text-align: center;
            font-size: 42px;
            font-weight: 300;
            color: white;
            margin-top: 30px;
            margin-bottom: 8px;
        }
        .accueil-sous-titre {
            text-align: center;
            font-size: 15px;
            color: #9e9e9e;
            margin-bottom: 40px;
        }
        .carte {
            background-color: #1e2029;
            border: 1px solid #2e3040;
            border-radius: 10px;
            padding: 24px 20px 20px 20px;
            cursor: pointer;
            transition: border-color 0.2s;
            min-height: 160px;
            position: relative;
        }
        .carte:hover {
            border-color: #1de9b6;
        }
        .carte-initiale {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background-color: #2e3040;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 700;
            color: #9e9e9e;
            margin-bottom: 16px;
        }
        .carte-titre {
            font-size: 16px;
            font-weight: 800;
            color: white;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        .carte-description {
            font-size: 13px;
            color: #9e9e9e;
        }
        .carte-fleche {
            position: absolute;
            bottom: 16px;
            right: 20px;
            font-size: 18px;
            color: #555;
        }
        </style>

        <div class="accueil-titre">Bienvenue</div>
        <div class="accueil-sous-titre">Sélectionnez un module pour accéder aux données détaillées.</div>
    """, unsafe_allow_html=True)

    # Récupérer les pages disponibles selon le rôle
    pages_dispo = st.session_state.get("pages_nav", {})

    # Ligne 1 : 3 cartes
    cols1 = st.columns(3)
    for i, module in enumerate(MODULES[:3]):
        with cols1[i]:
            _carte(module, pages_dispo)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Ligne 2 : 2 cartes + 1 espace
    cols2 = st.columns(3)
    for i, module in enumerate(MODULES[3:]):
        with cols2[i]:
            _carte(module, pages_dispo)


def _carte(module: dict, pages_dispo: dict):
    st.markdown(f"""
        <div class="carte">
            <div class="carte-initiale">{module["initiale"]}</div>
            <div class="carte-titre">{module["titre"]}</div>
            <div class="carte-description">{module["description"]}</div>
            <div class="carte-fleche">›</div>
        </div>
    """, unsafe_allow_html=True)

    page_obj = pages_dispo.get(module["page_title"])
    label = f"Accéder à {module['titre'].capitalize()}"
    if page_obj:
        if st.button(label, key=f"btn_{module['key']}", use_container_width=True):
            st.switch_page(page_obj)
    else:
        st.button(label, key=f"btn_{module['key']}", use_container_width=True, disabled=True)
