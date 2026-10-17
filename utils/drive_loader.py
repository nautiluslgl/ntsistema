import streamlit as st
import pandas as pd

ID_ANZUELOS = "TU_ID_DE_GOOGLE_DRIVE_ANZUELOS"
ID_GABRIEL = "TU_ID_DE_GOOGLE_DRIVE_GABRIEL"

def letra_a_indice(col):
    """Convierte letras de Excel ('A', 'B', 'E') o números a índices enteros de Python (0, 1, 4)."""
    if isinstance(col, int):
        return col
    col_str = str(col).strip().upper()
    if col_str.isdigit():
        return int(col_str)
    
    # Manejar letras de Excel (soporta 'A', 'B' ... hasta 'AA', 'AB')
    exp = 0
    idx = 0
    for char in reversed(col_str):
        if 'A' <= char <= 'Z':
            idx += (ord(char) - ord('A') + 1) * (26 ** exp)
            exp += 1
        else:
            return 0
    return idx - 1

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
    
    if nombre_hoja in CONFIG_GABRIEL:
        cfg = CONFIG_GABRIEL[nombre_hoja]
        header_row = int(cfg["fila_inicio"]) - 1
        
        df = pd.read_excel(url, sheet_name=nombre_hoja, header=header_row)

        # Convertir las letras requeridas a índices numéricos válidos
        cols_indices = [letra_a_indice(c) for c in cfg["columnas"]]
        cols_validas = [i for i in cols_indices if 0 <= i < df.shape[1]]
        
        df = df.iloc[:, cols_validas]
    else:
        df = pd.read_excel(url, sheet_name=nombre_hoja)

    df = df.dropna(how="all")
    return df
