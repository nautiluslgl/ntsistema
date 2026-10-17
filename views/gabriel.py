import streamlit as st
import pandas as pd
from utils.drive_loader import cargar_hoja_drive, ID_GABRIEL, CONFIG_GABRIEL, letra_a_indice
from utils.budget_manager import agregar_al_presupuesto, inicializar_presupuesto

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
                
                event = st.dataframe(
                    df, 
                    use_container_width=True,
                    on_select="rerun",
                    selection_mode="single-cell"
                )

                selection = event.get("selection", {}).get("cells", []) if event else []
                
                if selection:
                    try:
                        raw_row = selection[0][0]
                        raw_col = selection[0][1]

                        row_idx = int(raw_row) if str(raw_row).isdigit() else -1

                        if isinstance(raw_col, int) or str(raw_col).isdigit():
                            col_idx = int(raw_col)
                        else:
                            col_name_str = str(raw_col).strip()
                            col_idx = df.columns.get_loc(col_name_str) if col_name_str in df.columns else -1

                        if row_idx >= 0 and 0 <= col_idx < df.shape[1]:
                            cols_list = [str(c).lower() for c in cfg.get("columnas", [])]
                            col_bs_letra = str(cfg.get("col_bs", "")).lower()
                            col_usd_letra = str(cfg.get("col_usd", "")).lower()
                            col_prod_letra = str(cfg.get("col_producto", "")).lower()
                            
                            idx_bs = cols_list.index(col_bs_letra) if col_bs_letra in cols_list else -1
                            idx_usd = cols_list.index(col_usd_letra) if col_usd_letra in cols_list else -1
                            idx_prod = cols_list.index(col_prod_letra) if col_prod_letra in cols_list else 1

                            fila = df.iloc[row_idx]
                            
                            nombre_prod = str(fila.iloc[idx_prod]).strip() if (0 <= idx_prod < len(fila)) else f"Fila {row_idx + 1}"
                            
                            # Extraer marca si existe
                            marca_val = ""
                            for col_title in df.columns:
                                if "marca" in str(col_title).lower():
                                    val = str(fila[col_title]).strip()
                                    if val and val.lower() != "none" and val != ",":
                                        marca_val = val
                                    break

                            producto = f"{nombre_prod} ({marca_val})" if marca_val else nombre_prod

                            if col_idx == idx_bs or col_idx == idx_usd:
                                es_bs = (col_idx == idx_bs)
                                moneda = "Bs." if es_bs else "USD"
                                val_precio = fila.iloc[col_idx]
                                
                                # Consultar cuántos llevas actualmente en el presupuesto
                                inicializar_presupuesto()
                                cant_en_presupuesto = 0
                                for item in st.session_state.presupuesto:
                                    if item["producto"] == producto and item["hoja"] == hoja_actual:
                                        cant_en_presupuesto = item["cantidad"]
                                        break

                                st.info(f"📍 **Producto:** {producto} | **Precio ({moneda}):** {val_precio} | **En presupuesto:** {cant_en_presupuesto}")

                                # Botón con Key dinámico que se refresca al instante
                                btn_key = f"add_btn_{hoja_actual}_{row_idx}_{col_idx}_{cant_en_presupuesto}"

                                if st.button(f"➕ Añadir 1 a '{producto}' ({moneda})", key=btn_key, type="primary"):
                                    val_bs = fila.iloc[idx_bs] if idx_bs >= 0 else 0
                                    val_usd = fila.iloc[idx_usd] if idx_usd >= 0 else 0
                                    
                                    agregar_al_presupuesto(
                                        producto=producto,
                                        precio_bs=val_bs,
                                        precio_usd=val_usd,
                                        moneda=moneda,
                                        hoja=hoja_actual
                                    )
                                    st.rerun()
                            else:
                                st.warning("⚠️ Haz clic directamente sobre una celda de las columnas de **PRECIO** o **precio Bs** para activar el botón.")
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
