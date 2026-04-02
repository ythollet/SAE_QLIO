import streamlit as st
from utils.top_banner import func_top_banner
from page_production_2.kpi_taux_respect_delais import func_kpi_taux_respect_delais
from page_production_2.linechart_temps_cycle import func_linechart_temps_cycle
from page_production_2.linechart_taux_performance import func_linechart_taux_performance

def func_page_production_2():

    date_debut, date_fin = func_top_banner(key="prod2")

    func_kpi_taux_respect_delais(date_debut, date_fin)
    func_linechart_temps_cycle(date_debut, date_fin)
    func_linechart_taux_performance(date_debut, date_fin)
