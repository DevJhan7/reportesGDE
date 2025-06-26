# modules/pachambear.py
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
from utils.helpers import get_spanish_month, format_date

# Configuración de colores
CATEGORY_COLORS = {
    'Tecnología/Informática': '#3498db',
    'Administrativo': '#2ecc71',
    'Salud': '#e74c3c', 
    'Gastronomía': '#f39c12',
    'Transporte': '#9b59b6',
    'Seguridad': '#34495e',
    'Construcción': '#e67e22',
    'Ventas': '#1abc9c',
    'Limpieza/Mantenimiento': '#95a5a6',
    'Otros': '#7f8c8d'
}

CUL_COLORS = {
    'EMITIDO': '#27ae60',
    'BUSQUEDA': '#f39c12',
    'EN PROCESO': '#3498db',
    'Sin estado': '#bdc3c7'
}

def load_pachambear_data():
    """Carga y procesa los datos del CSV"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "reporte_pachambear2.csv"
        df = pd.read_csv(data_path, sep=';', encoding='utf-8')
        
        # Procesamiento de fechas
        df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True)
        df['MES'] = df['FECHA'].dt.month.map(get_spanish_month)
        
        # Limpieza de categorías
        df['CATEGORIA'] = df['CATEGORIA'].str.strip().fillna('Otros')
        df['CUL'] = df['CUL'].str.strip().fillna('Sin estado')
        
        return df
    
    except Exception as e:
        st.error(f"🚨 Error al cargar datos: {str(e)}")
        return None

def create_category_chart(df):
    """Gráfico de distribución por categoría"""
    st.markdown("### 🌈 Distribución por Categoría Laboral")
    
    category_counts = df['CATEGORIA'].value_counts().reset_index()
    fig = px.bar(
        category_counts,
        x='count',
        y='CATEGORIA',
        orientation='h',
        color='CATEGORIA',
        color_discrete_map=CATEGORY_COLORS,
        labels={'count': 'N° Solicitudes', 'CATEGORIA': ''},
        height=500,
        text='count'
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Número de Solicitudes"
    )
    
    fig.update_traces(
        textposition='outside',
        marker_line_color='rgba(8,48,107,0.6)',
        marker_line_width=1.5
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_cul_chart(df):
    """Gráfico de estados CUL"""
    st.markdown("### 📝 Estado de Certificados (CUL)")
    
    fig = px.pie(
        df,
        names='CUL',
        color='CUL',
        color_discrete_map=CUL_COLORS,
        hole=0.35,
        height=400
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=1))
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_trend_chart(df):
    """Gráfico de tendencia mensual"""
    st.markdown("### 📈 Tendencia Mensual de Solicitudes")
    
    monthly = df.groupby(['MES', 'FECHA']).size().reset_index(name='SOLICITUDES')
    monthly = monthly.sort_values('FECHA')
    
    fig = px.line(
        monthly,
        x='MES',
        y='SOLICITUDES',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#3498db'],
        height=400
    )
    
    fig.update_layout(
        xaxis_title='Mes',
        yaxis_title='Total Solicitudes'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_pachambear_module():
    """Módulo completo PACHAMBEAR"""
    st.header("📊 Módulo PACHAMBEAR - Reporte Laboral")
    st.markdown("---")
    
    with st.spinner("🔍 Cargando datos..."):
        df = load_pachambear_data()
    
    if df is not None:
        # Mostrar KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Período", 
                  f"{df['FECHA'].min().strftime('%d/%m/%Y')} - {df['FECHA'].max().strftime('%d/%m/%Y')}")
        col2.metric("🧑‍💼 Total Registros", len(df))
        col3.metric("🗂️ Categorías", df['CATEGORIA'].nunique())
        
        st.markdown("---")
        
        # Gráficos
        create_category_chart(df)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            create_cul_chart(df)
        with col2:
            create_trend_chart(df)
        
        # Datos crudos
        with st.expander("📁 Ver datos completos", expanded=False):
            st.dataframe(df)
