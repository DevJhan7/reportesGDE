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


def grafico_participantes(df, orden):
    participantes = df['FERIA'].value_counts().reset_index()
    participantes.columns = ['FERIA', 'N_PARTICIPANTES']

    # Agregar orden por fecha
    fechas = df.groupby("FERIA")['INGRESO'].min().reset_index()
    participantes = participantes.merge(fechas, on="FERIA")

    if orden == "Ascendente":
        participantes = participantes.sort_values("N_PARTICIPANTES")
    elif orden == "Descendente":
        participantes = participantes.sort_values("N_PARTICIPANTES", ascending=False)
    else:  # Por fecha
        participantes = participantes.sort_values("INGRESO")

    fig = px.bar(
        participantes,
        x='FERIA', y='N_PARTICIPANTES',
        title='👥 Participantes por Feria',
        color='FERIA', color_discrete_sequence=COLOR_MAP,
        text='N_PARTICIPANTES'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def grafico_recaudacion(df, orden):
    df['MONTO'] = pd.to_numeric(df['MONTO'], errors='coerce')
    recaudacion = df.groupby('FERIA')['MONTO'].sum().reset_index()
    fechas = df.groupby("FERIA")['INGRESO'].min().reset_index()
    recaudacion = recaudacion.merge(fechas, on="FERIA")

    if orden == "Ascendente":
        recaudacion = recaudacion.sort_values("MONTO")
    elif orden == "Descendente":
        recaudacion = recaudacion.sort_values("MONTO", ascending=False)
    else:  # Por fecha
        recaudacion = recaudacion.sort_values("INGRESO")

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


def grafico_trend_mensual(df):
    df_valid = df[df['INGRESO'].notna()]
    if df_valid.empty:
        st.info('No hay fechas para mostrar tendencia mensual.')
        return
    monthly = (
        df_valid.groupby(df_valid['INGRESO'].dt.to_period('M'))
        .size()
        .reset_index(name='INSCRIPCIONES')
    )
    monthly['MES_AÑO'] = monthly['INGRESO'].dt.to_timestamp()
    fig = px.line(
        monthly,
        x='MES_AÑO', y='INSCRIPCIONES',
        markers=True,
        line_shape='spline',
        title='📈 Tendencia Mensual de Inscripciones',
        color_discrete_sequence=['#3498db']
    )
    fig.update_xaxes(
        tickformat='%b %Y',
        tickmode='array',
        tickvals=monthly['MES_AÑO'],
        ticktext=monthly['MES_AÑO'].dt.strftime('%b %Y')
    )
    st.plotly_chart(fig, use_container_width=True)


def show_ferias_module():
    st.header('📊 Módulo de Ferias Laborales')
    st.markdown('---')

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

    if year == 'Histórico':
        dfs = []
        for y in ['2023', '2024', '2025']:
            d = load_ferias_data(y)
            if not d.empty:
                d = d.copy()
                d['AÑO'] = y
                dfs.append(d)
        df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
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

    # Selector de orden
    st.markdown('### Orden de gráficos')
    orden = st.selectbox("Ordenar por:", ["Por fecha", "Ascendente", "Descendente"])

    # Gráficos principales
    cA, cB = st.columns(2)
    with cA:
        grafico_participantes(df, orden)
    with cB:
        grafico_recaudacion(df, orden)

    st.markdown('---')
    grafico_macro_rubros(df)
    st.markdown('---')
    grafico_trend_mensual(df)

    # Histórico
    if year == 'Histórico':
        st.markdown('---')
        st.subheader('👥 Participantes Totales por Año')
        p_df = df['AÑO'].value_counts().reset_index()
        p_df.columns = ['AÑO', 'PARTICIPANTES']
        p_df = p_df.sort_values('AÑO')
        fig = px.bar(
            p_df,
            x='AÑO', y='PARTICIPANTES',
            color='AÑO', color_discrete_sequence=COLOR_MAP,
            text='PARTICIPANTES',
            title='Total de Participantes por Año'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


