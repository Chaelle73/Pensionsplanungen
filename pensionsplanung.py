import streamlit as st
import matplotlib.pyplot as plt

def pensionsplanung(alter, bvg_guthaben, umwandlungssatz, kapitalbezug, ahv_rente, private_vorsorge):
    # Berechnung der Altersrente aus BVG
    bvg_rente = (bvg_guthaben * (1 - kapitalbezug / 100)) * (umwandlungssatz / 100)
    
    # Monatliche Gesamtrente
    gesamt_rente = bvg_rente + ahv_rente + private_vorsorge
    
    # Daten für die Visualisierung
    jahre = list(range(alter, 90))  # Annahme: Lebenserwartung bis 90 Jahre
    einkommen = [gesamt_rente] * len(jahre)
    
    # Darstellung
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(jahre, einkommen, label='Jährliche Gesamtrente', marker='o')
    ax.set_xlabel('Alter')
    ax.set_ylabel('Jährliche Rente (CHF)')
    ax.set_title('Pensionsplanung: Renteneinkommen über die Jahre')
    ax.legend()
    ax.grid()
    
    return gesamt_rente, fig

st.title("Pensionsplanung Tool")

alter = st.slider("Alter", 55, 70, 65)
bvg_guthaben = st.number_input("BVG-Guthaben (CHF)", value=500000)
umwandlungssatz = st.slider("Umwandlungssatz (%)", 4.0, 7.0, 6.8, 0.1)
kapitalbezug = st.slider("Kapitalbezug (%)", 0, 100, 0, 10)
ahv_rente = st.number_input("AHV-Rente (CHF/Jahr)", value=28000)
private_vorsorge = st.number_input("Private Vorsorge (CHF/Jahr)", value=10000)

gesamt_rente, fig = pensionsplanung(alter, bvg_guthaben, umwandlungssatz, kapitalbezug, ahv_rente, private_vorsorge)

st.write(f"### Jährliche Altersrente: CHF {gesamt_rente:,.2f}")
st.pyplot(fig)
