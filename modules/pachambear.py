import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

def load_pachambear_data():
    """Carga automática del CSV desde la carpeta data"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "reporte_pachambear.csv"
        df = pd.read_csv(data_path, sep=';', encoding='utf-8')
        
        # Procesamiento básico
        df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True)
        df['MES'] = df['FECHA'].dt.month_name(locale='es')
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None

def show_pachambear_charts(df):
    """Genera los gráficos con títulos personalizados"""
    # --- Gráfico 1: Distribución por categoría ---
    st.markdown("### 📌 Gráfico 1: Distribución de Solicitudes por Categoría Laboral")
    fig1 = px.bar(
        df['CATEGORIA'].value_counts().reset_index(),
        x='count',
        y='CATEGORIA',
        orientation='h',
        labels={'count': 'N° Solicitudes', 'CATEGORIA': ''},
        color='CATEGORIA'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # --- Gráfico 2: Estados CUL ---
    st.markdown("### 📝 Gráfico 2: Estado de Certificados Únicos Laborales (CUL)")
    fig2 = px.pie(
        df['CUL'].value_counts().reset_index(),
        names='CUL',
        values='count',
        hole=0.3,
        labels={'count': 'Total'}
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # --- Gráfico 3: Tendencia mensual ---
    st.markdown("### 📈 Gráfico 3: Evolución Mensual de Solicitudes")
    monthly = df.groupby('MES').size().reset_index(name='SOLICITUDES')
    fig3 = px.line(
        monthly,
        x='MES',
        y='SOLICITUDES',
        markers=True,
        labels={'SOLICITUDES': 'Total Solicitudes', 'MES': 'Mes'}
    )
    st.plotly_chart(fig3, use_container_width=True)

def show_pachambear_module():
    """Módulo completo de PACHAMBEAR"""
    st.header("Módulo PACHAMBEAR")
    st.markdown("---")
    
    df = load_pachambear_data()
    if df is not None:
        show_pachambear_charts(df)