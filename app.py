import streamlit as st
from views.inicio import mostrar_inicio
from views.anzuelos import mostrar_vista as vista_anzuelos
from views.gabriel import mostrar_vista as vista_gabriel

# Configuración de página
st.set_page_config(page_title="Sistema de Gestión", layout="wide")

# Inicializar variables de estado para la navegación
if "opcion_seleccionada" not in st.session_state:
    st.session_state.opcion_seleccionada = None

if "hoja_anzuelos" not in st.session_state:
    st.session_state.hoja_anzuelos = None

if "hoja_gabriel" not in st.session_state:
    st.session_state.hoja_gabriel = None

# Enrutamiento de pantallas principales
if st.session_state.opcion_seleccionada is None:
    mostrar_inicio()
elif st.session_state.opcion_seleccionada == "anzuelos":
    vista_anzuelos()
elif st.session_state.opcion_seleccionada == "gabriel":
    vista_gabriel()
