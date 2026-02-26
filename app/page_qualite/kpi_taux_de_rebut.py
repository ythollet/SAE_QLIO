import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
import numpy as np
from utils.cnx_sql import func_query_sql_df

def func_kpi_taux_de_rebut():
    # ── 1. Requête SQL ──────────────────────────────────────────────
    query = """
        SELECT 
            SUM(CASE WHEN ErrorID != 0 THEN 1 ELSE 0 END) AS nok,
            COUNT(PNo) AS total
        FROM `tblpartsreport`
    """
    df = func_query_sql_df(query)

    if df.empty or df.iloc[0, 1] == 0:
        st.warning("Pas de données de production.")
        return

    nok = int(df.iloc[0, 0])
    total = int(df.iloc[0, 1])
    taux_rebut = round(nok / total * 100, 1)

    # Paramètres de la jauge
    LIMITE = 5
    MAX_VAL = 20
    TEAL = "#1de9b6"  # Vert/Teal
    RED = "#e05252"   # Rouge
    BG = "#111111"    # Fond sombre
    
    # Couleur du texte dynamique
    value_color = TEAL if taux_rebut <= LIMITE else RED

    # ── 2. Conversion valeur → angle ────────────────────────────────
    # 180° = Gauche (0%), 0° = Droite (MAX_VAL)
    def val_to_angle(v):
        return 180.0 - (min(v, MAX_VAL) / MAX_VAL) * 180.0

    angle_limite = val_to_angle(LIMITE)
    angle_aiguille = val_to_angle(taux_rebut)

    # ── 3. Figure matplotlib ────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.2, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

    R_OUTER = 1.0
    R_INNER = 0.65

    # ── Arc VERT : de la Limite (5%) jusqu'à la fin (20% -> 0°) ──
    # Note : Dans matplotlib Wedge, theta1 est l'angle de départ (sens anti-horaire)
    # Pour avoir le vert à gauche (0-5%), il faut qu'il soit entre 180° et angle_limite
    wedge_green = Wedge(
        center=(0, 0), r=R_OUTER, 
        theta1=angle_limite, theta2=180, 
        width=R_OUTER - R_INNER,
        facecolor=TEAL, edgecolor='none'
    )
    ax.add_patch(wedge_green)

    # ── Arc ROUGE : du début (0°) jusqu'à la Limite (5%) ──
    wedge_red = Wedge(
        center=(0, 0), r=R_OUTER, 
        theta1=0, theta2=angle_limite, 
        width=R_OUTER - R_INNER,
        facecolor=RED, edgecolor='none'
    )
    ax.add_patch(wedge_red)

    # ── 4. Aiguille BLANCHE ─────────────────────────────────────────
    needle_len = 0.85
    angle_rad = np.radians(angle_aiguille)
    
    # Coordonnées de la pointe
    tip_x = needle_len * np.cos(angle_rad)
    tip_y = needle_len * np.sin(angle_rad)

    # Dessin de l'aiguille (ligne blanche épaisse)
    ax.plot([0, tip_x], [0, tip_y], color='white', linewidth=5, solid_capstyle='round', zorder=10)

    # Petit pivot central blanc
    pivot = Circle((0, 0), radius=0.05, color='white', zorder=11)
    ax.add_patch(pivot)

    # ── 5. Texte et Titre ───────────────────────────────────────────
    # Affichage du % au centre
    ax.text(0, 0.35, f"{taux_rebut}%", ha='center', va='center', 
            fontsize=50, fontweight='bold', color=value_color)

    # Labels de graduation (Optionnel)
    ax.text(-1.1, -0.1, "0%", color='white', fontsize=12, ha='center')
    ax.text(1.1, -0.1, f"{MAX_VAL}%", color='white', fontsize=12, ha='center')
    ax.text(0, 1.1, "Taux de Rebut", color='white', fontsize=18, fontweight='bold', ha='center')

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)