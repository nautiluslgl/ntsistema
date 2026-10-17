import streamlit as st
import pandas as pd

# URLs / IDs de Google Drive
ID_ANZUELOS = "TU_ID_DE_GOOGLE_DRIVE_ANZUELOS"
ID_GABRIEL = "TU_ID_DE_GOOGLE_DRIVE_GABRIEL"

def letra_a_indice(letra):
    return ord(letra.upper()) - ord('A')

# Configuración extendida con mapeo de columnas para presupuesto
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
        "col_producto": "b", "col_bs": "e", "col_usd": "k"
    },
    "repuestos 75": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "i", "j", "k"],
        "col_producto": "b", "col_bs": "e", "col_usd": "k"
    },
    "Repuestos Suzuky(1)": {
        "fila_inicio": 2, 
        "columnas": ["a", "b", "e", "f", "g", "h", "i", "j", "k"],
        "col_producto": "b", "col_bs": "f", "col_usd": "j"
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
        header_row = cfg["fila_inicio"] - 1
        cols_indices = [letra_a_indice(c) for c in cfg["columnas"]]

        df = pd.read_excel(url, sheet_name=nombre_hoja, header=header_row)

        valid_indices = [i for i in cols_indices if i < len(df.columns)]
        df = df.iloc[:, valid_indices]
    else:
        df = pd.read_excel(url, sheet_name=nombre_hoja)

    df = df.dropna(how="all")
    return df
