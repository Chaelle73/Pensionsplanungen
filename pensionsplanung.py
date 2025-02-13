import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def pensionsplanung(alter, bvg_guthaben, umwandlungssatz, kapitalbezug, ahv_rente, gebundene_vorsorge, freie_vorsorge, private_vermoegen, verzinsung, kapitalverzehr_jahre, kapitalverzehr_jahresbetrag):
    # Berechnung der Altersrente aus BVG
    bvg_rente = (bvg_guthaben * (1 - kapitalbezug / 100)) * (umwandlungssatz / 100)
    
    # Monatliche Gesamtrente aus gebundener Vorsorge
    gebundene_rente = gebundene_vorsorge / kapitalverzehr_jahre if kapitalverzehr_jahre > 0 else 0
    
    # Kapitalverzehr für freie Vorsorge
    jahre = list(range(alter, alter + kapitalverzehr_jahre))
    kapitalverzehr = []
    restkapital = private_vermoegen
    gesamtes_einkommen = []
    
    for _ in jahre:
        entnahme = min(kapitalverzehr_jahresbetrag, restkapital)
        kapitalverzehr.append(entnahme)
        restkapital = (restkapital - entnahme) * (1 + verzinsung / 100)
        gesamtes_einkommen.append(bvg_rente + ahv_rente + gebundene_rente + entnahme)
    
    # Monatliche Gesamtrente
    gesamt_rente = bvg_rente + ahv_rente + gebundene_rente + (freie_vorsorge / kapitalverzehr_jahre if kapitalverzehr_jahre > 0 else 0)
    
    return gesamt_rente, kapitalverzehr, gesamtes_einkommen, jahre

st.title("Pensionsplanung Tool")

# Navigation
menu = st.sidebar.radio("Navigation", ["Personalien", "Einkommens- und Vermögensübersicht", "Vorsorgeanalyse", "Budgetplanung", "Steuerliche Planung", "Szenario-Analysen", "Grafische Darstellung"])

if menu == "Personalien":
    st.header("Personalien")
    name = st.text_input("Name")
    geburtsdatum = st.date_input("Geburtsdatum", value=datetime(1970, 1, 1))
    adresse = st.text_input("Adresse")
    wohnort = st.text_input("Wohnort")
    zivilstand = st.selectbox("Zivilstand", ["Ledig", "Verheiratet", "Geschieden", "Verwitwet"])
    partner_erfassen = st.checkbox("Partner/Partnerin erfassen")
    if partner_erfassen:
        partner_name = st.text_input("Partner/Partnerin Name")
        partner_geburtsdatum = st.date_input("Geburtsdatum Partner/Partnerin", value=datetime(1970, 1, 1))

if menu == "Einkommens- und Vermögensübersicht":
    st.header("Einkommens- und Vermögensübersicht")
    private_vermoegen = st.number_input("Privates Vermögen (CHF)", value=200000)
    ahv_rente = st.number_input("AHV-Rente (CHF/Jahr)", value=28000)

if menu == "Vorsorgeanalyse":
    st.header("Vorsorgeanalyse")
    bvg_guthaben = st.number_input("BVG-Guthaben (CHF)", value=500000)
    umwandlungssatz = st.slider("Umwandlungssatz (%)", 4.0, 7.0, 6.8, 0.1)
    kapitalbezug = st.slider("Kapitalbezug (%)", 0, 100, 0, 10)
    gebundene_vorsorge = st.number_input("Gebundene Vorsorge (CHF)", value=100000)
    freie_vorsorge = st.number_input("Freie Vorsorge (CHF)", value=50000)

if menu == "Budgetplanung":
    st.header("Budgetplanung")
    kapitalverzehr_jahre = st.slider("Kapitalverzehr über Jahre", 5, 30, 20)
    kapitalverzehr_jahresbetrag = st.number_input("Jährlicher Kapitalverzehr (CHF)", value=20000)
    verzinsung = st.slider("Verzinsung des Vermögens (%)", 0.0, 5.0, 1.0, 0.1)

if menu == "Steuerliche Planung":
    st.header("Steuerliche Planung")
    staffelung_3a = st.checkbox("Säule 3a gestaffelt beziehen?")
    if staffelung_3a:
        staffelungsjahre_3a = st.multiselect("Bezug Jahre für 3a", [f"{i+2024}" for i in range(0, 13)])

    staffelung_bvg = st.checkbox("BVG gestaffelt beziehen?")
    if staffelung_bvg:
        staffelungsjahre_bvg = st.multiselect("Bezug Jahre für BVG", [f"{i+2024}" for i in range(0, 13)])

if menu == "Grafische Darstellung":
    st.header("Grafische Darstellung")
    gesamt_rente, kapitalverzehr, gesamtes_einkommen, jahre = pensionsplanung(65, 500000, 6.8, 0, 28000, 100000, 50000, 200000, 1.0, 20, 20000)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(jahre, kapitalverzehr, label='Jährliche Kapitalentnahme', marker='o')
    ax.set_xlabel('Alter')
    ax.set_ylabel('Entnommenes Kapital (CHF)')
    ax.set_title('Kapitalverzehr über die Jahre')
    ax.legend()
    ax.grid()
    st.pyplot(fig)
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(jahre, gesamtes_einkommen, label='Jährliches Gesamteinkommen', marker='o', color='green')
    ax2.set_xlabel('Alter')
    ax2.set_ylabel('Gesamteinkommen (CHF)')
    ax2.set_title('Gesamteinkommen aus Renten und Kapitalverzehr')
    ax2.legend()
    ax2.grid()
    st.pyplot(fig2)
