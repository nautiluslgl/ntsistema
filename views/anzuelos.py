import streamlit as st
from utils.drive_loader import cargar_hoja_drive, ID_ANZUELOS

def mostrar_vista():
    st.subheader("🎣 Sección: Anzuelos y nailon detallado")

    if "hoja_anzuelos" not in st.session_state:
        st.session_state.hoja_anzuelos = None

    if st.session_state.hoja_anzuelos is None:
        st.write("Selecciona la pestaña u hoja que deseas consultar:")
        st.write("")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🏢 Maxi Industrias", use_container_width=True):
                st.session_state.hoja_anzuelos = "Maxi Industrias"
                st.rerun()

        with col2:
            if st.button("📄 Hoja1", use_container_width=True):
                st.session_state.hoja_anzuelos = "Hoja1"
                st.rerun()

        st.write("")
        st.divider()

        if st.button("← Volver al inicio principal"):
            st.session_state.opcion_seleccionada = None
            st.session_state.hoja_anzuelos = None
            st.rerun()

    else:
        st.subheader(f"Hoja: {st.session_state.hoja_anzuelos}")
        
        # Carga de datos
        try:
            with st.spinner("Cargando datos desde Google Drive..."):
                df = cargar_hoja_drive(ID_ANZUELOS, st.session_state.hoja_anzuelos)
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error al cargar la hoja: {e}")

        st.write("")
        col_back1, col_back2 = st.columns(2)
        
        with col_back1:
            if st.button("← Cambiar de hoja"):
                st.session_state.hoja_anzuelos = None
                st.rerun()
                
        with col_back2:
            if st.button("🏠 Menú Principal"):
                st.session_state.opcion_seleccionada = None
                st.session_state.hoja_anzuelos = None
                st.rerun()
