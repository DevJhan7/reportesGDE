import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
from utils.helpers import get_spanish_month

# Paleta de colores
COLOR_MAP = px.colors.qualitative.Set3

def load_ferias_data(year):
    """Carga datos procesados por año desde CSV con macro categorías"""
    archivo = Path(__file__).parent.parent / "data" / "ferias" / f"{year}_ferias_macro.csv"
    if not archivo.exists():
        return pd.DataFrame()

    df = pd.read_csv(archivo, sep=';', encoding='utf-8')
    # Procesar fecha
    if 'INGRESO' in df.columns:
        df['INGRESO'] = pd.to_datetime(df['INGRESO'], dayfirst=True, errors='coerce')
    elif 'FECHA DE INGRESO' in df.columns:
        df['INGRESO'] = pd.to_datetime(df['FECHA DE INGRESO'], dayfirst=True, errors='coerce')
    df['MES'] = df['INGRESO'].dt.month.map(get_spanish_month)
    return df

def grafico_participantes(df):
    participantes = df['FERIA'].value_counts().reset_index()
    participantes.columns = ['FERIA', 'N_PARTICIPANTES']
    participantes = participantes.sort_values('N_PARTICIPANTES')
    fig = px.bar(
        participantes,
        x='FERIA', y='N_PARTICIPANTES',
        title='👥 Participantes por Feria',
        color='FERIA', color_discrete_sequence=COLOR_MAP,
        text='N_PARTICIPANTES'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_recaudacion(df):
    df['MONTO'] = pd.to_numeric(df['MONTO'], errors='coerce')
    recaudacion = df.groupby('FERIA')['MONTO'].sum().reset_index()
    recaudacion = recaudacion.sort_values('MONTO')
    fig = px.bar(
        recaudacion,
        x='FERIA', y='MONTO',
        title='💰 Recaudación Total por Feria',
        color='FERIA', color_discrete_sequence=COLOR_MAP,
        text='MONTO'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_macro_rubros(df):
    rubros = df['MACRO_CATEGORIA'].value_counts().reset_index()
    rubros.columns = ['MACRO_CATEGORIA', 'CANTIDAD']
    fig = px.bar(
        rubros.head(10), x='MACRO_CATEGORIA', y='CANTIDAD',
        title='🏷️ Top 10 Macro Categorías',
        color='MACRO_CATEGORIA', color_discrete_sequence=COLOR_MAP,
        text='CANTIDAD'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_inscripciones(df):
    if df['INGRESO'].notna().any():
        diaria = df.groupby(df['INGRESO'].dt.date).size().reset_index(name='INSCRIPCIONES')
        fig = px.line(
            diaria, x='INGRESO', y='INSCRIPCIONES', markers=True,
            title='📈 Inscripciones Diarias',
            color_discrete_sequence=['#3498db']
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info('No hay fechas registradas para el periodo seleccionado.')

def show_ferias_module():
    st.header('📊 Módulo de Ferias Laborales')
    st.markdown('---')

    # Selección por botones
    if 'year_sel' not in st.session_state:
        st.session_state.year_sel = '2025'
    cols = st.columns(4)
    if cols[0].button('2023'):
        st.session_state.year_sel = '2023'
    if cols[1].button('2024'):
        st.session_state.year_sel = '2024'
    if cols[2].button('2025'):
        st.session_state.year_sel = '2025'
    if cols[3].button('Histórico'):
        st.session_state.year_sel = 'Histórico'

    year = st.session_state.year_sel
    st.markdown(f'**Año seleccionado:** {year}')

    # Cargar datos
    if year == 'Histórico':
        df_all = pd.concat(
            [load_ferias_data(y) for y in ['2023','2024','2025']],
            ignore_index=True
        )
        df = df_all
    else:
        df = load_ferias_data(year)

    if df.empty:
        st.warning('No se encontraron registros para la opción seleccionada.')
        return

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric('📆 Ferias', df['FERIA'].nunique())
    c2.metric('👥 Participantes', len(df))
    c3.metric('🏷️ Categorías', df['MACRO_CATEGORIA'].nunique())

    st.markdown('---')
    # Gráficos
    cA, cB = st.columns(2)
    with cA:
        grafico_participantes(df)
    with cB:
        grafico_recaudacion(df)

    st.markdown('---')
    grafico_macro_rubros(df)
    st.markdown('---')
    grafico_inscripciones(df)



