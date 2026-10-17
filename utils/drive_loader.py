import streamlit as st
import pandas as pd

ID_ANZUELOS = "1TIazPVWAkkN7xVwgJhMiRelhlYq2sa6k"
ID_GABRIEL = "1aD2C4665oaUSxtODfXSEvOQIvLJbwH3s"

def letra_a_indice(letra):
    """Convierte letras de Excel ('A', 'B', 'E') a índice numérico base 0."""
    l = str(letra).strip().upper()
    return ord(l) - ord('A')

CONFIG_GABRIEL = {
    "articulos de pesca": {
        "fila_inicio": 3, 
        "columnas": ["b", "c", "d", "e"],
        "col_producto": "b", "col_bs": "d", "col_usd": "e"
    },
    "40x burbuja": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "j"],
        "col_producto": "b", "col_bs": "e", "col_usd": "j"
    },
    "40g cuadrado": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "j"],
        "col_producto": "b", "col_bs": "e", "col_usd": "j"
    },
    "repuestos 75": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "i", "j", "k"],
        "col_producto": "b", "col_bs": "e", "col_usd": "k"
    },
    "Repuestos Suzuky(1)": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "i", "j", "k"],
        "col_producto": "b", "col_bs": "e", "col_usd": "k"
    },
    "Repuestos Tohatsu": {
        "fila_inicio": 1, 
        "columnas": ["a", "b", "c", "d", "e", "g", "h"],
        "col_producto": "b", "col_bs": "e", "col_usd": "h"
    },
    "repuestos 25": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "h", "j", "k"],
        "col_producto": "b", "col_bs": "e", "col_usd": "k"
    },
    "REPUESTOS 48": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "d", "f", "g", "h", "j", "k"],
        "col_producto": "b", "col_bs": "d", "col_usd": "k"
    },
    "REPUESTOS 15,2HP": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "f", "g", "h", "i", "j", "k"],
        "col_producto": "b", "col_bs": "f", "col_usd": "k"
    },
    "REPUESTOS 5,8,60,70,30": {
        "fila_inicio": 3, 
        "columnas": ["a", "b", "c", "e", "f", "h"],
        "col_producto": "b", "col_bs": "e", "col_usd": "h"
    }
}
@st.cache_data(ttl=600)
def cargar_hoja_drive(id_archivo, nombre_hoja):
    url = f"https://docs.google.com/spreadsheets/d/{id_archivo}/export?format=xlsx"
    
    # Buscar configuración ignorando diferencias de mayúsculas/minúsculas
    config_encontrada = None
    for clave, cfg in CONFIG_GABRIEL.items():
        if clave.strip().lower() == str(nombre_hoja).strip().lower():
            config_encontrada = cfg
            break

    if config_encontrada:
        # Fila de inicio convertida de forma segura
        header_row = int(config_encontrada.get("fila_inicio", 2)) - 1
        
        df = pd.read_excel(url, sheet_name=nombre_hoja, header=header_row)

        cols_indices = [letra_a_indice(c) for c in config_encontrada.get("columnas", [])]
        cols_validas = [i for i in cols_indices if 0 <= i < df.shape[1]]
        
        df = df.iloc[:, cols_validas]
    else:
        df = pd.read_excel(url, sheet_name=nombre_hoja)

    df = df.dropna(how="all")
    return df
