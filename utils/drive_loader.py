import streamlit as st
import pandas as pd

ID_ANZUELOS = "1TIazPVWAkkN7xVwgJhMiRelhlYq2sa6k"
ID_GABRIEL = "1aD2C4665oaUSxtODfXSEvOQIvLJbwH3s"

def letra_a_indice(letra):
    """Convierte letras de Excel ('A', 'B', 'E') a índice base 0 de Python."""
    return ord(str(letra).strip().upper()) - ord('A')

CONFIG_GABRIEL = {
    "articulos de pesca": {
        "fila_inicio": 3, 
        "columnas": ["b", "c", "d", "e"]
    },
    "40x burbuja": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "j"]
    },
    "40g cuadrado": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "j"]
    },
    "repuestos 75": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "i", "j", "k"]
    },
    "Repuestos Suzuky(1)": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "i", "j", "k"]
    },
    "Repuestos Tohatsu": {
        "fila_inicio": 1, 
        "columnas": ["a", "b", "c", "d", "e", "g", "h"]
    },
    "repuestos 25": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "h", "j", "k"]
    },
    "REPUESTOS 48": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "d", "f", "g", "h", "j", "k"]
    },
    "REPUESTOS 15,2HP": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "f", "g", "h", "i", "j", "k"]
    },
    "REPUESTOS 5,8,60,70,30": {
        "fila_inicio": 3, 
        "columnas": ["a", "b", "c", "e", "f", "h"]
    }
}

@st.cache_data(ttl=600)
def cargar_hoja_drive(id_archivo, nombre_hoja):
    url = f"https://docs.google.com/spreadsheets/d/{id_archivo}/export?format=xlsx"
    
    if nombre_hoja in CONFIG_GABRIEL:
        cfg = CONFIG_GABRIEL[nombre_hoja]
        header_row = int(cfg["fila_inicio"]) - 1
        
        # Leer el Excel respetando la fila de encabezado
        df = pd.read_excel(url, sheet_name=nombre_hoja, header=header_row)

        # Seleccionar únicamente los índices numéricos de las columnas indicadas
        cols_indices = [letra_a_indice(c) for c in cfg["columnas"]]
        cols_validas = [i for i in cols_indices if 0 <= i < df.shape[1]]
        
        df = df.iloc[:, cols_validas]
    else:
        df = pd.read_excel(url, sheet_name=nombre_hoja)

    # Limpieza de filas completamente vacías
    df = df.dropna(how="all")
    return df
