import streamlit as st

def mostrar_vista():
    st.subheader("🎣 Sección: Anzuelos y nailon detallado")
    st.info("Aquí cargaremos y mostraremos las tablas de 'anzuelos y nailon detallado(1).xlsx'")

    if st.button("← Volver al inicio"):
        st.session_state.opcion_seleccionada = None
        st.rerun()
