import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
from utils.helpers import get_spanish_month, format_date

def load_pachambear_data():
    """Carga y procesa los datos usando helpers"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "reporte_pachambear.csv"
        df = pd.read_csv(data_path, sep=';', encoding='utf-8')
        
        # Procesamiento con funciones de helpers
        df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True)
        df['MES'] = df['FECHA'].dt.month.map(get_spanish_month)
        df['FECHA_FORMATEADA'] = df['FECHA'].dt.strftime('%d/%m/%Y').apply(format_date)
        
        # Limpieza
        df['CATEGORIA'] = df['CATEGORIA'].str.strip().fillna('Sin categoría')
        df['CUL'] = df['CUL'].str.strip().fillna('Sin estado')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None

def show_pachambear_charts(df):
    """Genera gráficos interactivos"""
    # Gráfico 1 - Distribución por categoría
    st.markdown("### 📊 Distribución por Categoría Laboral")
    category_counts = df['CATEGORIA'].value_counts().reset_index()
    fig1 = px.bar(category_counts, x='count', y='CATEGORIA', orientation='h')
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2 - Estados CUL
    st.markdown("### 📝 Estado de Certificados")
    fig2 = px.pie(df, names='CUL', hole=0.3)
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3 - Tendencia mensual
    st.markdown("### 📈 Tendencia Mensual")
    monthly = df.groupby('MES', observed=True).size().reset_index(name='SOLICITUDES')
    fig3 = px.line(monthly, x='MES', y='SOLICITUDES', markers=True)
    st.plotly_chart(fig3, use_container_width=True)

def show_pachambear_module():
    """Módulo principal"""
    st.header("🔍 Módulo PACHAMBEAR")
    with st.spinner("Cargando datos..."):
        df = load_pachambear_data()
    
    if df is not None:
        show_pachambear_charts(df)
        with st.expander("🔎 Ver datos crudos"):
            st.dataframe(df)
