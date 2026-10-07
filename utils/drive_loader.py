import streamlit as st
import pandas as pd

# URLs de descarga directa desde Google Drive
# NOTA: Reemplaza los IDs con los de tus enlaces de Google Drive
ID_ANZUELOS = "1eIzHhvSmKLKaj9VucmpdqC3A0jCL6Uj3"
ID_GABRIEL = "1OC4F7B9qxpnLXCIHe7EGBTHxyZ47_twp"

def letra_a_indice(letra):
    return ord(letra.upper()) - ord('A')

CONFIG_GABRIEL = {
    "articulos de pesca": {"fila_inicio": 3, "columnas": ["b", "c", "d", "e"]},
    "40x burbuja": {"fila_inicio": 2, "columnas": ["a", "b", "e", "f", "g", "h", "j"]},
    "40g cuadrado": {"fila_inicio": 2, "columnas": ["a", "b", "e", "f", "g", "h", "K"]},
    "repuestos 75": {"fila_inicio": 2, "columnas": ["a", "b", "e", "f", "g", "i", "j", "k"]},
    "Repuestos Suzuky(1)": {"fila_inicio": 2, "columnas": ["a", "b", "e", "f", "g", "h", "i", "j", "k"]},
    "Repuestos Tohatsu": {"fila_inicio": 1, "columnas": ["a", "b", "c", "d", "e", "g", "h"]},
    "repuestos 25": {"fila_inicio": 2, "columnas": ["a", "b", "e", "f", "h", "j", "k"]},
    "REPUESTOS 48": {"fila_inicio": 2, "columnas": ["a", "b", "d", "f", "g", "h", "j", "k"]},
    "REPUESTOS 15,2HP": {"fila_inicio": 2, "columnas": ["a", "b", "f", "g", "h", "i", "j", "k"]},
    "REPUESTOS 5,8,60,70,30": {"fila_inicio": 3, "columnas": ["a", "b", "c", "e", "f", "h"]}
}

@st.cache_data(ttl=600)  # Guarda en caché la lectura por 10 minutos para mayor rapidez
def cargar_hoja_drive(id_archivo, nombre_hoja):
    url = f"https://docs.google.com/spreadsheets/d/{id_archivo}/export?format=xlsx"
    
    # Verificar si la hoja tiene configuración de filas y columnas personalizada
    if nombre_hoja in CONFIG_GABRIEL:
        cfg = CONFIG_GABRIEL[nombre_hoja]
        header_row = cfg["fila_inicio"] - 1  # Pandas usa índice 0 para las filas
        cols_indices = [letra_a_indice(c) for c in cfg["columnas"]]

        # Leer Excel desde la fila deseada
        df = pd.read_excel(url, sheet_name=nombre_hoja, header=header_row)

        # Filtrar únicamente las columnas seleccionadas que existan en la tabla
        valid_indices = [i for i in cols_indices if i < len(df.columns)]
        df = df.iloc[:, valid_indices]
    else:
        # Lectura por defecto si no está en el diccionario
        df = pd.read_excel(url, sheet_name=nombre_hoja)

    # Eliminar filas completamente vacías al final de la tabla
    df = df.dropna(how="all")

    return df
