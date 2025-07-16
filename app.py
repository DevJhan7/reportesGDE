import streamlit as st
from modules.pachambear import show_pachambear_module
from modules.ferias import show_ferias_module

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Reportes Municipales",
    page_icon="📊",
    layout="wide"
)

# Sidebar de navegación
st.sidebar.title("📁 Navegación")
modulo = st.sidebar.radio(
    "Seleccione un módulo:",
    ("PACHAMBEAR", "FERIAS", "Otros reportes")
)

# Encabezado principal
st.title("📋 Reportes Estadísticos de la Gerencia de Licencias y Desarrollo Económico")
st.markdown("---")

# Mostrar módulo seleccionado
if modulo == "PACHAMBEAR":
    show_pachambear_module()
elif modulo == "FERIAS":
    show_ferias_module()
else:
    st.info("⚙️ Módulo en desarrollo. Próximamente disponible.")
