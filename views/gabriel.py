import streamlit as st

def mostrar_vista():
    st.subheader("📦 Sección: Gabriel 5")
    st.write("Selecciona la pestaña u hoja que deseas consultar:")

    # Inicializar estado para la hoja elegida en Gabriel 5
    if "hoja_gabriel" not in st.session_state:
        st.session_state.hoja_gabriel = None

    # Lista de hojas disponibles
    hojas = [
        "articulos de pesca",
        "40x burbuja",
        "40g cuadrado",
        "repuestos 75",
        "Repuestos Suzuky(1)",
        "Repuestos Tohatsu",
        "repuestos 25",
        "REPUESTOS 48",
        "REPUESTOS 15,2HP",
        "REPUESTOS 5,8,60,70,30"
    ]

    # Si no ha seleccionado hoja, mostramos los botones en 2 columnas
    if st.session_state.hoja_gabriel is None:
        st.write("")
        col1, col2 = st.columns(2)
        
        for i, hoja in enumerate(hojas):
            # Alternar entre columna 1 y columna 2
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(f"📄 {hoja}", key=f"btn_gabriel_{i}", use_container_width=True):
                    st.session_state.hoja_gabriel = hoja
                    st.rerun()

        st.write("")
        st.divider()

        if st.button("← Volver al inicio principal"):
            st.session_state.opcion_seleccionada = None
            st.session_state.hoja_gabriel = None
            st.rerun()

    # Si ya seleccionó una hoja, mostramos su vista
    else:
        st.info(f"Visualizando la hoja: **{st.session_state.hoja_gabriel}**")
        
        st.write("*(Próximamente: Tabla de datos cargada desde Google Drive)*")

        st.write("")
        col_back1, col_back2 = st.columns(2)
        
        with col_back1:
            if st.button("← Cambiar de hoja"):
                st.session_state.hoja_gabriel = None
                st.rerun()
                
        with col_back2:
            if st.button("🏠 Menú Principal"):
                st.session_state.opcion_seleccionada = None
                st.session_state.hoja_gabriel = None
                st.rerun()
