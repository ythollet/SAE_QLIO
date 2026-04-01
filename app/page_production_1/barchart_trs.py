import streamlit as st
import altair as alt
import pandas as pd
from utils.cnx_sql import func_query_sql_df

def func_barchart_trs(temps_planifie_h: int, date_debut=None, date_fin=None):

    temps_cycle_theorique = 500  # secondes
    temps_planifie_s = temps_planifie_h * 3600

    filtre_parts = (
        f"WHERE DATE(TimeStamp) BETWEEN '{date_debut}' AND '{date_fin}'"
        if date_debut
        else ""
    )
    filtre_machine = (
        f"AND DATE(TimeStamp) BETWEEN '{date_debut}' AND '{date_fin}'"
        if date_debut
        else ""
    )

    # ── Taux de Qualité ──────────────────────────────────────────────
    # tblpartsreport(PNo, ErrorID) : pièces OK / total
    df_q = func_query_sql_df(f"""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN ErrorID = 0 THEN 1 ELSE 0 END) AS nb_ok
        FROM tblpartsreport
        {filtre_parts}
    """)
    total_pieces = int(df_q.iloc[0, 0])
    nb_ok = int(df_q.iloc[0, 1])
    taux_qualite = nb_ok / total_pieces if total_pieces > 0 else 0

    # ── Taux de Disponibilité ────────────────────────────────────────
    # tblmachinereport(AutomaticMode, Busy, ErrorL0/L1/L2, TimeStamp)
    # Durée des états où AutomaticMode=1, Busy=1, pas d'erreur
    # via LEAD(TimeStamp) pour calculer la durée de chaque état
    df_d = func_query_sql_df(f"""
        WITH etats AS (
            SELECT
                TimeStamp,
                AutomaticMode, Busy, ErrorL0, ErrorL1, ErrorL2,
                LEAD(TimeStamp) OVER (PARTITION BY ResourceID ORDER BY TimeStamp) AS next_ts
            FROM tblmachinereport
        )
        SELECT
            SUM(CASE
                WHEN AutomaticMode = 1 AND Busy = 1
                     AND ErrorL0 = 0 AND ErrorL1 = 0 AND ErrorL2 = 0
                THEN TIMESTAMPDIFF(SECOND, TimeStamp, next_ts)
                ELSE 0
            END) AS temps_fonctionnement_s,
            COUNT(DISTINCT DATE(TimeStamp)) AS nb_jours
        FROM etats
        WHERE next_ts IS NOT NULL
        {filtre_machine}
    """)
    temps_fonctionnement_s = float(df_d.iloc[0, 0] if df_d.iloc[0, 0] is not None else 0)
    nb_jours = int(df_d.iloc[0, 1] or 1)
    temps_planifie_total_s = temps_planifie_s * nb_jours
    taux_dispo = min(temps_fonctionnement_s / temps_planifie_total_s, 1.0) if temps_planifie_total_s > 0 else 0

    # ── Taux de Performance ──────────────────────────────────────────
    # (nb_pieces × temps_cycle_theorique) / temps_fonctionnement
    taux_perf = min((total_pieces * temps_cycle_theorique) / temps_fonctionnement_s, 1.0) if temps_fonctionnement_s > 0 else 0

    # ── DataFrame ────────────────────────────────────────────────────
    df = pd.DataFrame({
        'composante': ['DISPONIBILITÉ', 'PERFORMANCE', 'QUALITÉ'],
        'valeur': [taux_dispo * 100, taux_perf * 100, taux_qualite * 100]
    })

    cible = 85  # % cible par composante

    barres = alt.Chart(df).mark_bar(cornerRadius=4).encode(
        x=alt.X(
            'composante:N',
            axis=alt.Axis(title='COMPOSANTE DU TRS', titleFontWeight='bold', labelAngle=0),
            sort=None
        ),
        y=alt.Y(
            'valeur:Q',
            scale=alt.Scale(domain=[0, 100]),
            axis=alt.Axis(title='TAUX EN POURCENTAGE', titleFontWeight='bold', format='.0f')
        ),
        color=alt.condition(
            alt.datum.valeur >= cible,
            alt.value('#1de9b6'),
            alt.value('#555555')
        )
    ).properties(
        height=350,
        title=alt.TitleParams(
            text='DÉCOMPOSITION DU TRS (DISPONIBILITÉ, PERFORMANCE, QUALITÉ)',
            anchor='middle',
            fontSize=13,
            fontWeight='bold'
        )
    )

    etiquettes = barres.mark_text(
        dy=-14, fontSize=14, fontWeight='bold', color='white'
    ).encode(
        text=alt.Text('valeur:Q', format='.1f')
    )

    df_cible = pd.DataFrame({'cible': [cible]})
    ligne_cible = alt.Chart(df_cible).mark_rule(
        color='red', strokeDash=[6, 4]
    ).encode(y='cible:Q')

    texte_cible = alt.Chart(df_cible).mark_text(
        align='right', dx=-4, dy=-6, color='red', fontSize=11
    ).encode(
        y='cible:Q',
        x=alt.value(310),
        text=alt.value(f'CIBLE PAR COMPOSANTE ({cible}%)')
    )

    st.altair_chart(barres + etiquettes + ligne_cible + texte_cible, use_container_width=True)
