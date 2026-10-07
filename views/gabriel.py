import streamlit as st
from utils.drive_loader import cargar_hoja_drive, ID_GABRIEL

def mostrar_vista():
    st.subheader("📦 Sección: Gabriel 5")

    if "hoja_gabriel" not in st.session_state:
        st.session_state.hoja_gabriel = None

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

    if st.session_state.hoja_gabriel is None:
        st.write("Selecciona la pestaña u hoja que deseas consultar:")
        st.write("")
        col1, col2 = st.columns(2)
        
        for i, hoja in enumerate(hojas):
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

    else:
        st.subheader(f"Hoja: {st.session_state.hoja_gabriel}")
        
        # Carga de datos
        try:
            with st.spinner("Cargando datos desde Google Drive..."):
                df = cargar_hoja_drive(ID_GABRIEL, st.session_state.hoja_gabriel)
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error al cargar la hoja: {e}")

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
