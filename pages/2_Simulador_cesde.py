import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.write("Simulador Cesde")
try:
    df = pd.read_csv('static/cesde.csv')
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()

# Obtener las opciones únicas de cada filtro
gruposU = sorted(df['GRUPO'].unique())
nivelesU = sorted(df['NIVEL'].unique())
jornadasU = sorted(df['JORNADA'].unique())
horarioU = sorted(df['HORARIO'].unique())
submodulosU = sorted(df['SUBMODULO'].unique())
docentesU = sorted(df['DOCENTE'].unique())
momentosU = sorted(df['MOMENTO'].unique())

# Configurar las columnas y selectores
col1, col2, col3, col4 = st.columns(4)

with col1:
    gruposU.insert(0, "Todos")
    optionGrupo = st.selectbox('Grupo', (gruposU))

with col2:       
    optionMomento = st.selectbox('Momento', (momentosU))

with col3:
    nivelesU.insert(0, "Todos")
    optionNivel = st.selectbox('Nivel', (nivelesU))

with col4:
    jornadasU.insert(0, "Todos")
    optionJornada = st.selectbox('Jornada', (jornadasU))

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionGrupo != 'Todos':
    filtered_data = filtered_data[filtered_data['GRUPO'] == optionGrupo]

if optionMomento:
    filtered_data = filtered_data[filtered_data['MOMENTO'] == optionMomento]

if optionNivel != 'Todos':
    filtered_data = filtered_data[filtered_data['NIVEL'] == optionNivel]

if optionJornada != 'Todos':
    filtered_data = filtered_data[filtered_data['JORNADA'] == optionJornada]

# Crear el gráfico de barras
if not filtered_data.empty:
    NOTAS = filtered_data['NOMBRE']
    fig = go.Figure(data=[
        go.Bar(name='CONOCIMIENTO', x=NOTAS, y=filtered_data['CONOCIMIENTO']),
        go.Bar(name='DESEMPEÑO', x=NOTAS, y=filtered_data['DESEMPEÑO']),
        go.Bar(name='PRODUCTO', x=NOTAS, y=filtered_data['PRODUCTO'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No hay datos disponibles para los filtros seleccionados.")

# Gráfico 1: Nivel
if not filtered_data.empty:
    grouped_data = filtered_data.groupby('NIVEL').mean()
    fig2 = go.Figure(data=[
        go.Bar(name='CONOCIMIENTO', x=grouped_data.index, y=grouped_data['CONOCIMIENTO']),
        go.Bar(name='DESEMPEÑO', x=grouped_data.index, y=grouped_data['DESEMPEÑO']),
        go.Bar(name='PRODUCTO', x=grouped_data.index, y=grouped_data['PRODUCTO'])
    ])
    fig2.update_layout(barmode='stack')
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico 2: Momento
if not filtered_data.empty:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=filtered_data['MOMENTO'], y=filtered_data['CONOCIMIENTO'], mode='lines+markers', name='CONOCIMIENTO'))
    fig3.add_trace(go.Scatter(x=filtered_data['MOMENTO'], y=filtered_data['DESEMPEÑO'], mode='lines+markers', name='DESEMPEÑO'))
    fig3.add_trace(go.Scatter(x=filtered_data['MOMENTO'], y=filtered_data['PRODUCTO'], mode='lines+markers', name='PRODUCTO'))
    st.plotly_chart(fig3, use_container_width=True)

# Gráfico 3: distribución de estudiantes por Nivel
if not filtered_data.empty:
    nivel_counts = filtered_data['NIVEL'].value_counts()
    fig4 = go.Figure(data=[go.Pie(labels=nivel_counts.index, values=nivel_counts.values)])
    st.plotly_chart(fig4, use_container_width=True)