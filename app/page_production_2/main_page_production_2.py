import streamlit as st
from utils.date_filter import func_date_filter
from page_production_2.kpi_taux_respect_delais import func_kpi_taux_respect_delais
from page_production_2.linechart_taux_performance import func_linechart_taux_performance

def func_page_production_2():

    date_debut, date_fin = func_date_filter(key="prod2")

    func_kpi_taux_respect_delais(date_debut, date_fin)

    func_linechart_taux_performance(date_debut, date_fin)
