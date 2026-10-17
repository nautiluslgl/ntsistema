import streamlit as st
from views.inicio import mostrar_inicio
from views.anzuelos import mostrar_vista as vista_anzuelos
from views.gabriel import mostrar_vista as vista_gabriel

# Configuración de página
st.set_page_config(page_title="Sistema de Gestión y Presupuestos", layout="wide")

# 1. Inicializar variables de estado global
if "opcion_seleccionada" not in st.session_state:
    st.session_state.opcion_seleccionada = None

if "hoja_anzuelos" not in st.session_state:
    st.session_state.hoja_anzuelos = None

if "hoja_gabriel" not in st.session_state:
    st.session_state.hoja_gabriel = None

# Lista global para acumular los ítems del presupuesto
if "presupuesto" not in st.session_state:
    st.session_state.presupuesto = []

# 2. Barra Lateral (Sidebar) - Panel del Presupuesto Activo
with st.sidebar:
    st.header("📋 Presupuesto Activo")
    
    if len(st.session_state.presupuesto) == 0:
        st.info("No has agregado ningún ítem al presupuesto.")
    else:
        st.write(f"**Ítems agregados:** {len(st.session_state.presupuesto)}")
        
        # Mostrar resumen rápido de los ítems
        total_bs = 0.0
        total_usd = 0.0
        
        for idx, item in enumerate(st.session_state.presupuesto, 1):
            st.markdown(f"**{idx}.** {item['producto']}")
            st.caption(f"Precio: {item['precio_bs']} Bs | {item['precio_usd']} USD")
            total_bs += float(item.get('precio_bs', 0) or 0)
            total_usd += float(item.get('precio_usd', 0) or 0)
            st.divider()

        st.markdown(f"### **Total Bs:** {total_bs:,.2f}")
        st.markdown(f"### **Total USD:** {total_usd:,.2f}")

        col_side1, col_side2 = st.columns(2)
        with col_side1:
            if st.button("🧹 Limpiar", use_container_width=True):
                st.session_state.presupuesto = []
                st.rerun()

        with col_side2:
            if st.button("💾 Guardar", use_container_width=True):
                st.success("Guardado (Próximamente en Drive/DB)")

# 3. Enrutamiento de pantallas principales
if st.session_state.opcion_seleccionada is None:
    mostrar_inicio()
elif st.session_state.opcion_seleccionada == "anzuelos":
    vista_anzuelos()
elif st.session_state.opcion_seleccionada == "gabriel":
    vista_gabriel()
