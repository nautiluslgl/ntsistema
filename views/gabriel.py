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
        
        if selection:
    try:
        # Intentar obtener la fila y columna como enteros de forma segura
        raw_row = selection[0][0]
        raw_col = selection[0][1]

        # Si por alguna razón la columna viene como texto ('PRECIO'), la convertimos con letra_a_indice
        from utils.drive_loader import letra_a_indice
        
        row_idx = int(raw_row) if str(raw_row).isdigit() else -1
        col_idx = int(raw_col) if str(raw_col).isdigit() else letra_a_indice(raw_col)

        if row_idx >= 0 and col_idx >= 0:
            cols_list = [str(c).lower() for c in cfg.get("columnas", [])]
            col_bs_letra = str(cfg.get("col_bs", "")).lower()
            col_usd_letra = str(cfg.get("col_usd", "")).lower()
            col_prod_letra = str(cfg.get("col_producto", "")).lower()
            
            idx_bs = cols_list.index(col_bs_letra) if col_bs_letra in cols_list else -1
            idx_usd = cols_list.index(col_usd_letra) if col_usd_letra in cols_list else -1
            idx_prod = cols_list.index(col_prod_letra) if col_prod_letra in cols_list else 1

            fila = df.iloc[row_idx]
            
            if col_idx < len(fila):
                producto = str(fila.iloc[idx_prod]) if (0 <= idx_prod < len(fila)) else f"Fila {row_idx + 1}"

                if col_idx == idx_bs or col_idx == idx_usd:
                    es_bs = (col_idx == idx_bs)
                    moneda = "Bs." if es_bs else "USD"
                    val_precio = fila.iloc[col_idx]
                    
                    st.info(f"📍 **Producto:** {producto} | **Precio ({moneda}):** {val_precio}")

                    if st.button(f"➕ Añadir '{producto}' ({moneda}) al Presupuesto", type="primary"):
                        val_bs = fila.iloc[idx_bs] if idx_bs >= 0 else 0
                        val_usd = fila.iloc[idx_usd] if idx_usd >= 0 else 0
                        
                        st.session_state.presupuesto.append({
                            "producto": producto,
                            "precio_bs": val_bs,
                            "precio_usd": val_usd,
                            "moneda_seleccionada": moneda,
                            "hoja": hoja_actual
                        })
                        st.success(f"¡'{producto}' añadido al presupuesto!")
                        st.rerun()
                else:
                    st.warning("⚠️ Haz clic directamente sobre una celda de las columnas de **Precio** para activar el botón de agregar.")
    except Exception as sel_err:
        st.warning("Selecciona una celda de precio válida.")

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
