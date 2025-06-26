import streamlit as st
from modules.pachambear import show_pachambear_module

# Configuración de la página
st.set_page_config(
    page_title="Sistema PACHAMBEAR",
    page_icon="📋",
    layout="wide"
)

# Sidebar
st.sidebar.title("Navegación")
modulo = st.sidebar.radio(
    "Seleccione módulo:",
    ("PACHAMBEAR", "Otros reportes")
)

# Contenido principal
st.title("📋 Sistema de Reportes Laborales")
st.markdown("---")

if modulo == "PACHAMBEAR":
    show_pachambear_module()
else:
    st.info("Módulo en desarrollo")
