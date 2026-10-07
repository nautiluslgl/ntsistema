import streamlit as st
import pandas as pd

# URLs de descarga directa desde Google Drive
# NOTA: Reemplaza los IDs con los de tus enlaces de Google Drive
ID_ANZUELOS = "1eIzHhvSmKLKaj9VucmpdqC3A0jCL6Uj3"
ID_GABRIEL = "1OC4F7B9qxpnLXCIHe7EGBTHxyZ47_twp"

@st.cache_data(ttl=600)  # Guarda en caché la lectura por 10 minutos para mayor rapidez
def cargar_hoja_drive(id_archivo, nombre_hoja):
    url = f"https://docs.google.com/spreadsheets/d/{id_archivo}/export?format=xlsx"
    df = pd.read_excel(url, sheet_name=nombre_hoja)
    return df
