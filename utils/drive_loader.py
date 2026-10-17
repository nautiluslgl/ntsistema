import streamlit as st
import pandas as pd

# 1. Variables de IDs requeridas por las otras vistas
ID_ANZUELOS = "1TIazPVWAkkN7xVwgJhMiRelhlYq2sa6k"
ID_GABRIEL = "1aD2C4665oaUSxtODfXSEvOQIvLJbwH3s"


def letra_a_indice(letra):
    """Convierte posiciones o letras de Excel a índice base 0 ignorando nombres de texto."""
    if isinstance(letra, int):
        return letra
    
    col_str = str(letra).strip()
    
    # Si es un número en texto ej. "5"
    if col_str.isdigit():
        return int(col_str)
    
    # Si es estrictamente una letra de columna de Excel (ej: "A", "B", "E", "J")
    if col_str.isalpha():
        col_str_upper = col_str.upper()
        idx = 0
        for char in col_str_upper:
            idx = idx * 26 + (ord(char) - ord('A') + 1)
        return idx - 1
        
    # Si recibe un encabezado de texto (ej: 'precio Bs', 'NOMBRE'), lo ignora devolviendo -1
    return -1


# 2. Configuración de Gabriel
CONFIG_GABRIEL = {
    "articulos de pesca": {
        "fila_inicio": 3, 
        "columnas": ["b", "c", "d", "e"],
        "col_producto": "b", "col_bs": "d", "col_usd": "e"
    },
    "40x burbuja": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "j"],
        "col_producto": "b", "col_bs": "j", "col_usd": "e"
    },
    "40g cuadrado": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "j"],
        "col_producto": "b", "col_bs": "j", "col_usd": "e"
    },
    "repuestos 75": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "i", "j", "k"],
        "col_producto": "b", "col_bs": "k", "col_usd": "e"
    },
    "Repuestos Suzuky(1)": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "i", "j", "k"],
        "col_producto": "b", "col_bs": "k", "col_usd": "e"
    },
    "Repuestos Tohatsu": {
        "fila_inicio": 1, 
        "columnas": ["a", "b", "c", "d", "e", "g", "h"],
        "col_producto": "b", "col_bs": "h", "col_usd": "e"
    },
    "repuestos 25": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "h", "j", "k"],
        "col_producto": "b", "col_bs": "k", "col_usd": "e"
    },
    "REPUESTOS 48": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "d", "f", "g", "h", "j", "k"],
        "col_producto": "b", "col_bs": "k", "col_usd": "d"
    },
    "REPUESTOS 15,2HP": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "f", "g", "h", "i", "j", "k"],
        "col_producto": "b", "col_bs": "k", "col_usd": "f"
    },
    "REPUESTOS 5,8,60,70,30": {
        "fila_inicio": 3, 
        "columnas": ["a", "b", "c", "e", "f", "h"],
        "col_producto": "b", "col_bs": "h", "col_usd": "e"
    }
}


@st.cache_data(ttl=600)
def cargar_hoja_drive(id_archivo, nombre_hoja):
    url = f"https://docs.google.com/spreadsheets/d/{id_archivo}/export?format=xlsx"
    
    config_encontrada = None
    for clave, cfg in CONFIG_GABRIEL.items():
        if clave.strip().lower() == str(nombre_hoja).strip().lower():
            config_encontrada = cfg
            break

    if config_encontrada:
        header_row = int(config_encontrada.get("fila_inicio", 2)) - 1
        df = pd.read_excel(url, sheet_name=nombre_hoja, header=header_row)

        cols_indices = [letra_a_indice(c) for c in config_encontrada.get("columnas", [])]
        cols_validas = [i for i in cols_indices if 0 <= i < df.shape[1]]
        
        if cols_validas:
            df = df.iloc[:, cols_validas]
    else:
        df = pd.read_excel(url, sheet_name=nombre_hoja)

    df = df.dropna(how="all")
    return df
