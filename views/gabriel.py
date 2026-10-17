import streamlit as st
from utils.drive_loader import cargar_hoja_drive, ID_GABRIEL, CONFIG_GABRIEL

def mostrar_vista():
    st.subheader("📦 Sección: Gabriel 5")

    if "hoja_gabriel" not in st.session_state:
        st.session_state.hoja_gabriel = None

    hojas = list(CONFIG_GABRIEL.keys())

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
        hoja_actual = st.session_state.hoja_gabriel
        st.subheader(f"Hoja: {hoja_actual}")
        
        try:
            with st.spinner("Cargando datos desde Google Drive..."):
                df = cargar_hoja_drive(ID_GABRIEL, hoja_actual)
                
                # Renderizar tabla interactiva con selección de celda
                event = st.dataframe(
                    df, 
                    use_container_width=True,
                    on_select="rerun",
                    selection_mode="single-cell"
                )

                # Verificar celda seleccionada
                selection = event.get("selection", {}).get("cells", [])
                if selection:
                    row_idx, col_idx = selection[0]
                    nombre_columna = df.columns[col_idx]
                    
                    cfg = CONFIG_GABRIEL.get(hoja_actual, {})
                    
                    # Obtener producto y precios de la fila seleccionada
                    fila = df.iloc[row_idx]
                    producto = str(fila.iloc[1]) if len(fila) > 1 else f"Ítem fila {row_idx+1}"
                    
                    val_bs = fila.iloc[2] if len(fila) > 2 else 0
                    val_usd = fila.iloc[-1] if len(fila) > 0 else 0

                    st.info(f"📍 **Seleccionado:** {producto} | **Columna:** {nombre_columna}")

                    if st.button(f"➕ Añadir '{producto}' al Presupuesto", type="primary"):
                        st.session_state.presupuesto.append({
                            "producto": producto,
                            "precio_bs": val_bs,
                            "precio_usd": val_usd,
                            "hoja": hoja_actual
                        })
                        st.success(f"¡'{producto}' agregado con éxito!")
                        st.rerun()

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
