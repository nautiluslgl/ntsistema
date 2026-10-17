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
                
                # Renderizar tabla interactiva con selección de celdas
                event = st.dataframe(
                    df, 
                    use_container_width=True,
                    on_select="rerun",
                    selection_mode="single-cell"
                )

                # Detección de celda seleccionada
                selection = event.get("selection", {}).get("cells", [])
                if selection:
                    row_idx, col_idx = selection[0]
                    row_idx = int(row_idx)
                    col_idx = int(col_idx)
                    
                    # Nombre del encabezado de la columna tocada
                    nombre_columna = str(df.columns[col_idx]).strip()
                    nombre_col_lower = nombre_columna.lower()
                    
                    # Fila seleccionada
                    fila = df.iloc[row_idx]
                    
                    # Asumimos que la descripción del producto es la segunda columna útil (índice 1)
                    producto = str(fila.iloc[1]) if len(fila) > 1 else f"Fila {row_idx + 1}"
                    valor_celda = fila.iloc[col_idx]

                    # Validar si la columna seleccionada corresponde a un precio (Bs o USD)
                    # Detecta palabras clave en el encabezado
                    es_bs = any(k in nombre_col_lower for k in ["bs", "bolivar", "bolívares"])
                    es_usd = any(k in nombre_col_lower for k in ["usd", "$", "dolar", "dólar", "precio"])
                    
                    # Si la columna es de precios
                    if es_bs or es_usd or ("precio" in nombre_col_lower):
                        moneda = "Bs." if es_bs else ("USD" if es_usd else "Monto")
                        
                        st.info(f"📍 **Producto:** {producto} | **{nombre_columna}:** {valor_celda}")

                        if st.button(f"➕ Añadir '{producto}' ({moneda}: {valor_celda}) al Presupuesto", type="primary"):
                            precio_bs = valor_celda if es_bs else 0
                            precio_usd = valor_celda if es_usd else 0
                            
                            st.session_state.presupuesto.append({
                                "producto": producto,
                                "precio_bs": precio_bs,
                                "precio_usd": precio_usd,
                                "moneda": moneda,
                                "hoja": hoja_actual
                            })
                            st.success(f"¡'{producto}' agregado al presupuesto!")
                            st.rerun()
                    else:
                        st.warning(f"⚠️ Has seleccionado la columna **'{nombre_columna}'**. Por favor, haz clic directamente en una celda de las columnas de **Precio (Bs. o USD)** para poder agregarlo.")

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
