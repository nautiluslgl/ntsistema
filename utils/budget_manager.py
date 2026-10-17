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


def generar_texto_cotizacion():
    """Genera el texto con el formato exacto para copiar y pegar en WhatsApp."""
    if not st.session_state.presupuesto:
        return ""

    # Determinar la moneda predominante seleccionada por el usuario
    monedas = [item.get("moneda_seleccionada", "Bs.") for item in st.session_state.presupuesto]
    es_usd = monedas.count("USD") > monedas.count("Bs.")

    lineas = []
    total_general = 0.0

    if es_usd:
        lineas.append("Cotización Ref (USD):")
        for item in st.session_state.presupuesto:
            cant = item.get("cantidad", 1)
            precio_unit = item["precio_usd"]
            subtotal = precio_unit * cant
            total_general += subtotal
            lineas.append(f"{cant} {item['producto']} ${precio_unit:.2f} | Total: ${subtotal:.2f}")
        lineas.append(f"\nTOTAL: ${total_general:.2f}")
    else:
        lineas.append("Cotización:")
        for item in st.session_state.presupuesto:
            cant = item.get("cantidad", 1)
            precio_unit = item["precio_bs"]
            subtotal = precio_unit * cant
            total_general += subtotal
            lineas.append(f"{cant} {item['producto']} Bs {precio_unit:.2f} | Total: Bs {subtotal:.2f}")
        lineas.append(f"\nTOTAL: Bs {total_general:.2f}")

    return "\n".join(lineas)


def renderizar_sidebar_presupuesto():
    """Dibuja el panel lateral con opción de copiar cotización."""
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

        st.sidebar.markdown(f"**{idx}. {cant}x {item['producto']}**")
        st.sidebar.caption(f"Precio: {subtotal_bs:,.2f} Bs | {subtotal_usd:,.2f} USD")
        st.sidebar.divider()

    st.sidebar.markdown(f"### Total Bs: {total_bs:,.2f}")
    st.sidebar.markdown(f"### Total USD: {total_usd:,.2f}")

    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("🧹 Limpiar", use_container_width=True):
            st.session_state.presupuesto = []
            st.session_state.mostrar_cotizacion = False
            st.rerun()

    with col_btn2:
        if st.button("📋 Copiar", use_container_width=True, type="primary"):
            st.session_state.mostrar_cotizacion = True

    # Desplegar el cuadro de texto para copiar al presionar "📋 Copiar"
    if st.session_state.get("mostrar_cotizacion", False):
        st.sidebar.success("¡Texto listo! Haz clic en el botón de copiar (arriba a la derecha del cuadro):")
        texto_cotizacion = generar_texto_cotizacion()
        st.sidebar.code(texto_cotizacion, language="text")
