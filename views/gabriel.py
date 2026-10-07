import streamlit as st

def mostrar_vista():
    st.subheader("📦 Sección: Gabriel 5")
    st.info("Aquí cargaremos y mostraremos las tablas de 'GABRIEL5 precios mayo 26 (1).xlsx'")

    if st.button("← Volver al inicio"):
        st.session_state.opcion_seleccionada = None
        st.rerun()
