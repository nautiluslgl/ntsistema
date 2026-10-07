import streamlit as st

# Configuración de la página (modo ancho y título)
st.set_page_config(page_title="Sistema de Consultas", layout="wide")

# Título principal centrado
st.markdown("<h1 style='text-align: center;'>Bienvenido al Sistema de Gestión</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Selecciona una opción para consultar los datos</p>", unsafe_allow_html=True)

st.write("") # Espacio en blanco
st.write("") 

# Inicializar la variable de navegación si no existe
if "opcion_seleccionada" not in st.session_state:
    st.session_state.opcion_seleccionada = None

# Crear 3 columnas para centrar los botones (la columna del centro contendrá los botones)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Botón 1
    if st.button("🎣 Anzuelos y nailon detallado", use_container_width=True):
        st.session_state.opcion_seleccionada = "anzuelos"

    st.write("") # Espaciado entre botones

    # Botón 2
    if st.button("📦 Gabriel 5", use_container_width=True):
        st.session_state.opcion_seleccionada = "gabriel"

# --- VISTAS / CONTENIDO DE CADA SECCIÓN ---
st.divider()

if st.session_state.opcion_seleccionada == "anzuelos":
    st.subheader("Sección: Anzuelos y nailon detallado")
    st.info("Aquí cargaremos y mostraremos los datos de 'anzuelos y nailon detallado(1).xlsx'")
    
    # Botón para volver al menú o cambiar
    if st.button("← Volver al inicio"):
        st.session_state.opcion_seleccionada = None
        st.rerun()

elif st.session_state.opcion_seleccionada == "gabriel":
    st.subheader("Sección: Gabriel 5")
    st.info("Aquí cargaremos y mostraremos los datos de 'GABRIEL5 precios mayo 26 (1).xlsx'")
    
    # Botón para volver al menú o cambiar
    if st.button("← Volver al inicio"):
        st.session_state.opcion_seleccionada = None
        st.rerun()
