import streamlit as st
import pandas as pd

def inicializar_presupuesto():
    if "presupuesto" not in st.session_state:
        st.session_state.presupuesto = []


def agregar_al_presupuesto(producto, precio_bs, precio_usd, moneda, hoja):
    inicializar_presupuesto()

    try:
        val_bs = float(precio_bs) if pd.notnull(precio_bs) else 0.0
    except (ValueError, TypeError):
        val_bs = 0.0

    try:
        val_usd = float(precio_usd) if pd.notnull(precio_usd) else 0.0
    except (ValueError, TypeError):
        val_usd = 0.0

    # Buscar coincidencia por producto y hoja
    encontrado = False
    for item in st.session_state.presupuesto:
        if item["producto"] == producto and item["hoja"] == hoja:
            item["cantidad"] += 1
            encontrado = True
            break

    if not encontrado:
        st.session_state.presupuesto.append({
            "producto": producto,
            "precio_bs": val_bs,
            "precio_usd": val_usd,
            "cantidad": 1,
            "moneda_seleccionada": moneda,
            "hoja": hoja
        })


def renderizar_sidebar_presupuesto():
    """Dibuja el panel lateral calculando subtotales por cantidad acumulada."""
    inicializar_presupuesto()

    st.sidebar.markdown("## 📋 Presupuesto Activo")

    if not st.session_state.presupuesto:
        st.sidebar.info("El presupuesto está vacío.")
        return

    total_bs = 0.0
    total_usd = 0.0
    total_items = sum(item.get("cantidad", 1) for item in st.session_state.presupuesto)

    st.sidebar.write(f"**Ítems agregados:** {total_items}")
    st.sidebar.divider()

    for idx, item in enumerate(st.session_state.presupuesto, start=1):
        cant = item.get("cantidad", 1)
        subtotal_bs = item["precio_bs"] * cant
        subtotal_usd = item["precio_usd"] * cant

        total_bs += subtotal_bs
        total_usd += subtotal_usd

        # Texto acumulado (ej. 1. 11x Anodo externo (METALBAI))
        texto_item = f"**{idx}. {cant}x {item['producto']}**" if cant > 1 else f"**{idx}. {item['producto']}**"
        st.sidebar.markdown(texto_item)
        st.sidebar.caption(f"Precio: {subtotal_bs:,.2f} Bs | {subtotal_usd:,.2f} USD")
        st.sidebar.divider()

    st.sidebar.markdown(f"### Total Bs: {total_bs:,.2f}")
    st.sidebar.markdown(f"### Total USD: {total_usd:,.2f}")

    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("🧹 Limpiar", use_container_width=True):
            st.session_state.presupuesto = []
            st.rerun()
    with col_btn2:
        if st.button("💾 Guardar", use_container_width=True):
            st.sidebar.success("Presupuesto guardado")
