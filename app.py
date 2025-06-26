import streamlit as st
from modules.pachambear import show_pachambear_module

# Configuración de página
st.set_page_config(
    page_title="Sistema de Reportes Laborales",
    page_icon="📋",
    layout="wide"
)

# Sidebar con navegación
st.sidebar.title("🏗️ Módulos Disponibles")
modulo_activo = st.sidebar.radio(
    "Seleccione el área:",
    ("PACHAMBEAR", "OTRO_MODULO")  # Añadir más módulos aquí
)

# Título principal
st.title("📋 CUADRO DE ATENCIÓN AL ADMINISTRADO")
st.markdown("**Sistema Integrado de Bolsa de Trabajo y Certificado Único Laboral**")
st.markdown("---")

# Cargar módulo seleccionado
if modulo_activo == "PACHAMBEAR":
    show_pachambear_module()
else:
    st.warning("Módulo en desarrollo")