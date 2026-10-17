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
                cfg = CONFIG_GABRIEL.get(hoja_actual, {})
                
                # Renderizar tabla interactiva
                event = st.dataframe(
                    df, 
                    use_container_width=True,
                    on_select="rerun",
                    selection_mode="single-cell"
                )

                # Detección de celda
                selection = event.get("selection", {}).get("cells", [])
                if selection:
                    row_idx, col_idx = selection[0]
                    row_idx = int(row_idx)
                    col_idx = int(col_idx)
                    
                    cols_list = cfg.get("columnas", [])
                    col_bs_letra = str(cfg.get("col_bs", "")).lower()
                    col_usd_letra = str(cfg.get("col_usd", "")).lower()
                    
                    # Identificar posiciones relativas
                    idx_bs = cols_list.index(col_bs_letra) if col_bs_letra in cols_list else -1
                    idx_usd = cols_list.index(col_usd_letra) if col_usd_letra in cols_list else -1

                    fila = df.iloc[row_idx]
                    
                    # Producto (columna B de la tabla)
                    producto = str(fila.iloc[1]) if len(fila) > 1 else f"Fila {row_idx + 1}"

                    if col_idx == idx_bs or col_idx == idx_usd:
                        tipo_precio = "Bs." if col_idx == idx_bs else "USD"
                        val_precio = fila.iloc[col_idx]
                        
                        st.info(f"📍 **Producto:** {producto} | **Precio ({tipo_precio}):** {val_precio}")

                        if st.button(f"➕ Añadir '{producto}' al Presupuesto", type="primary"):
                            val_bs = fila.iloc[idx_bs] if idx_bs >= 0 else 0
                            val_usd = fila.iloc[idx_usd] if idx_usd >= 0 else 0
                            
                            st.session_state.presupuesto.append({
                                "producto": producto,
                                "precio_bs": val_bs,
                                "precio_usd": val_usd,
                                "moneda": tipo_precio,
                                "hoja": hoja_actual
                            })
                            st.success(f"¡'{producto}' agregado con éxito!")
                            st.rerun()
                    else:
                        st.warning("⚠️ Selecciona una celda de la columna de precio (Bs. o USD) para habilitar el botón de agregar.")

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
