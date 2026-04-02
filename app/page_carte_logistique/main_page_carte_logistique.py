import streamlit as st
import plotly.graph_objects as go


# Coordonnées réelles
SITES = [
    {
        "nom": "Usine T'Elefan",
        "adresse": "IUT Lyon 2 — Lyon, France",
        "lat": 45.7485,
        "lon": 4.8467,
        "couleur": "#1de9b6",
        "role": "Usine de production",
    },
    {
        "nom": "Festo Didactic SE",
        "adresse": "Rechbergstr. 3, 73770 Denkendorf, Allemagne",
        "lat": 48.6947,
        "lon": 9.3145,
        "couleur": "#ff9800",
        "role": "Client",
    },
]


def func_page_carte_logistique():
    st.markdown("## Carte Chaîne Logistique")

    # ── Carte Plotly ────────────────────────────────────────────────
    fig = go.Figure()

    # Ligne entre les deux sites
    fig.add_trace(go.Scattergeo(
        lon=[SITES[0]["lon"], SITES[1]["lon"]],
        lat=[SITES[0]["lat"], SITES[1]["lat"]],
        mode="lines",
        line=dict(width=2, color="#1de9b6"),
        hoverinfo="skip",
        showlegend=False,
    ))

    # Marqueurs
    for site in SITES:
        fig.add_trace(go.Scattergeo(
            lon=[site["lon"]],
            lat=[site["lat"]],
            mode="markers+text",
            marker=dict(size=14, color=site["couleur"], symbol="circle"),
            text=[site["nom"]],
            textposition="top center",
            textfont=dict(color="white", size=13),
            hovertemplate=(
                f"<b>{site['nom']}</b><br>"
                f"{site['adresse']}<br>"
                f"<i>{site['role']}</i><extra></extra>"
            ),
            name=site["nom"],
        ))

    fig.update_layout(
        geo=dict(
            scope="europe",
            showland=True,
            landcolor="#1e2029",
            showocean=True,
            oceancolor="#111111",
            showcoastlines=True,
            coastlinecolor="#444",
            showframe=False,
            countrycolor="#333",
            showcountries=True,
            center=dict(lat=47.2, lon=7.0),
            projection_scale=4.5,
        ),
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font=dict(color="white"),
        legend=dict(
            bgcolor="#1e2029",
            bordercolor="#444",
            x=0.01, y=0.99
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)
