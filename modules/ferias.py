import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
from utils.helpers import get_spanish_month

# Paleta de colores
COLOR_MAP = px.colors.qualitative.Set3

def load_ferias_data(year):
    """Carga archivo unificado por año con clasificación y limpieza previa"""
    archivo = Path(__file__).parent.parent / "data" / "ferias" / f"{year}_ferias_macro.csv"
    if not archivo.exists():
        return pd.DataFrame()

    df = pd.read_csv(archivo, sep=';', encoding='utf-8')

    if 'INGRESO' in df.columns:
        df["INGRESO"] = pd.to_datetime(df["INGRESO"], dayfirst=True, errors="coerce")
        df["MES"] = df["INGRESO"].dt.month.map(get_spanish_month)
    elif 'FECHA DE INGRESO' in df.columns:
        df["INGRESO"] = pd.to_datetime(df["FECHA DE INGRESO"], dayfirst=True, errors="coerce")
        df["MES"] = df["INGRESO"].dt.month.map(get_spanish_month)

    return df

def grafico_participantes(df):
    participantes = df["FERIA"].value_counts().reset_index()
    participantes.columns = ["FERIA", "N_PARTICIPANTES"]
    participantes = participantes.sort_values("N_PARTICIPANTES")  # orden ascendente

    fig = px.bar(participantes, x="FERIA", y="N_PARTICIPANTES",
                 title="👥 Participantes por Feria",
                 color="FERIA", color_discrete_sequence=COLOR_MAP,
                 text="N_PARTICIPANTES")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_recaudacion(df):
    df["MONTO"] = pd.to_numeric(df["MONTO"], errors="coerce")
    recaudacion = df.groupby("FERIA")["MONTO"].sum().reset_index()
    recaudacion = recaudacion.sort_values("MONTO")  # orden ascendente

    fig = px.bar(recaudacion, x="FERIA", y="MONTO",
                 title="💰 Recaudación Total por Feria",
                 color="FERIA", color_discrete_sequence=COLOR_MAP,
                 text="MONTO")
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_macro_rubros(df):
    rubros = df["MACRO_CATEGORIA"].value_counts().reset_index()
    rubros.columns = ["MACRO_CATEGORIA", "CANTIDAD"]
    fig = px.bar(rubros.head(10), x="MACRO_CATEGORIA", y="CANTIDAD",
                 title="🏷️ Top 10 Macro Categorías",
                 color="MACRO_CATEGORIA", color_discrete_sequence=COLOR_MAP,
                 text="CANTIDAD")
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_inscripciones(df):
    diaria = df.groupby(df["INGRESO"].dt.date).size().reset_index(name="INSCRIPCIONES")
    fig = px.line(diaria, x="INGRESO", y="INSCRIPCIONES", markers=True,
                  title="📈 Inscripciones Diarias",
                  color_discrete_sequence=["#3498db"])
    st.plotly_chart(fig, use_container_width=True)

def show_ferias_module():
    st.header("📊 Módulo de Ferias Laborales")
    st.markdown("---")

    anio = st.selectbox("Seleccionar año:", options=["2023", "2024", "2025"], index=1)

    with st.spinner("Cargando datos..."):
        df = load_ferias_data(anio)

    if df.empty:
        st.warning("No se encontraron registros para el año seleccionado.")
        return

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("📆 Ferias registradas", df["FERIA"].nunique())
    col2.metric("👥 Total participantes", len(df))
    col3.metric("🏷️ Categorías agrupadas", df["MACRO_CATEGORIA"].nunique())

    st.markdown("---")

    # Gráficos lado a lado
    col_a, col_b = st.columns(2)
    with col_a:
        grafico_participantes(df)
    with col_b:
        grafico_recaudacion(df)

    st.markdown("---")
    grafico_macro_rubros(df)
    st.markdown("---")
    grafico_inscripciones(df)



