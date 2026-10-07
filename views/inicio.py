import streamlit as st

def mostrar_inicio():
    st.markdown("<h1 style='text-align: center;'>Bienvenido al Sistema de Gestión</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Selecciona una opción para consultar los datos</p>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🎣 Anzuelos y nailon detallado", use_container_width=True):
            st.session_state.opcion_seleccionada = "anzuelos"
            st.rerun()

        st.write("")

        if st.button("📦 Gabriel 5", use_container_width=True):
            st.session_state.opcion_seleccionada = "gabriel"
            st.rerun()
