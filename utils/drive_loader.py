import streamlit as st
import pandas as pd

# URLs de descarga directa desde Google Drive
# NOTA: Reemplaza los IDs con los de tus enlaces de Google Drive
ID_ANZUELOS = "https://docs.google.com/spreadsheets/d/1eIzHhvSmKLKaj9VucmpdqC3A0jCL6Uj3/edit?usp=drive_link&ouid=100716700891760015236&rtpof=true&sd=true"
ID_GABRIEL = "https://docs.google.com/spreadsheets/d/1OC4F7B9qxpnLXCIHe7EGBTHxyZ47_twp/edit?usp=drive_link&ouid=100716700891760015236&rtpof=true&sd=true"

@st.cache_data(ttl=600)  # Guarda en caché la lectura por 10 minutos para mayor rapidez
def cargar_hoja_drive(id_archivo, nombre_hoja):
    url = f"https://docs.google.com/spreadsheets/d/{id_archivo}/export?format=xlsx"
    df = pd.read_excel(url, sheet_name=nombre_hoja)
    return df
