import streamlit as st

def mostrar_vista():
    st.subheader("🎣 Sección: Anzuelos y nailon detallado")
    st.write("Selecciona la pestaña u hoja que deseas consultar:")

    # Inicializar estado para la hoja elegida
    if "hoja_anzuelos" not in st.session_state:
        st.session_state.hoja_anzuelos = None

    # Si aún no ha seleccionado ninguna hoja, mostramos los botones
    if st.session_state.hoja_anzuelos is None:
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

    # Si ya seleccionó una hoja, mostramos su contenido y opción de regresar
    else:
        st.info(f"Visualizando la hoja: **{st.session_state.hoja_anzuelos}**")
        
        # Aquí cargaremos la tabla correspondiente a la hoja elegida
        st.write("*(Próximamente: Tabla de datos cargada desde Google Drive)*")

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
