import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def pensionsplanung(alter, bvg_guthaben, umwandlungssatz, kapitalbezug, ahv_rente, gebundene_vorsorge, freie_vorsorge, private_vermoegen, verzinsung, kapitalverzehr_jahre):
    # Berechnung der Altersrente aus BVG
    bvg_rente = (bvg_guthaben * (1 - kapitalbezug / 100)) * (umwandlungssatz / 100)
    
    # Monatliche Gesamtrente aus gebundener Vorsorge
    gebundene_rente = gebundene_vorsorge / kapitalverzehr_jahre if kapitalverzehr_jahre > 0 else 0
    
    # Kapitalverzehr für freie Vorsorge
    jahre = list(range(alter, alter + kapitalverzehr_jahre))
    kapitalverzehr = []
    restkapital = private_vermoegen
    for _ in jahre:
        entnahme = restkapital / (kapitalverzehr_jahre if kapitalverzehr_jahre > 0 else 1)
        kapitalverzehr.append(entnahme)
        restkapital = (restkapital - entnahme) * (1 + verzinsung / 100)
    
    # Monatliche Gesamtrente
    gesamt_rente = bvg_rente + ahv_rente + gebundene_rente + (freie_vorsorge / kapitalverzehr_jahre if kapitalverzehr_jahre > 0 else 0)
    
    # Darstellung
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(jahre, kapitalverzehr, label='Jährliche Kapitalentnahme', marker='o')
    ax.set_xlabel('Alter')
    ax.set_ylabel('Entnommenes Kapital (CHF)')
    ax.set_title('Kapitalverzehr über die Jahre')
    ax.legend()
    ax.grid()
    
    return gesamt_rente, fig

st.title("Pensionsplanung Tool")

alter = st.slider("Alter", 55, 70, 65)
bvg_guthaben = st.number_input("BVG-Guthaben (CHF)", value=500000)
umwandlungssatz = st.slider("Umwandlungssatz (%)", 4.0, 7.0, 6.8, 0.1)
kapitalbezug = st.slider("Kapitalbezug (%)", 0, 100, 0, 10)
ahv_rente = st.number_input("AHV-Rente (CHF/Jahr)", value=28000)
gebundene_vorsorge = st.number_input("Gebundene Vorsorge (CHF)", value=100000)
freie_vorsorge = st.number_input("Freie Vorsorge (CHF)", value=50000)
private_vermoegen = st.number_input("Privates Vermögen (CHF)", value=200000)
verzinsung = st.slider("Verzinsung des Vermögens (%)", 0.0, 5.0, 1.0, 0.1)
kapitalverzehr_jahre = st.slider("Kapitalverzehr über Jahre", 5, 30, 20)

gesamt_rente, fig = pensionsplanung(alter, bvg_guthaben, umwandlungssatz, kapitalbezug, ahv_rente, gebundene_vorsorge, freie_vorsorge, private_vermoegen, verzinsung, kapitalverzehr_jahre)

st.write(f"### Jährliche Altersrente: CHF {gesamt_rente:,.2f}")
st.pyplot(fig)
