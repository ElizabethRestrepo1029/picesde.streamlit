import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar el tema de Streamlit
st.set_page_config(
    page_title="Control de rutas",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Leer el archivo CSV
try:
    df = pd.read_csv('static/controlruta.csv')
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()
# Filtrar y seleccionar solo las columnas relevantes
df_filt = df[['VEHICULO', 'CONDUCTOR', 'ESTADO']]

# Eliminar filas con valores nulos en las columnas seleccionadas
df_filt = df_filt.dropna()

# Filtros
filtro_vehiculo = st.selectbox('Selecciona un vehículo:', ['Todos'] + list(df_filt['VEHICULO'].unique()))
if filtro_vehiculo != 'Todos':
    df_filt = df_filt[df_filt['VEHICULO'] == filtro_vehiculo]

filtro_conductor = st.selectbox('Selecciona un conductor:', ['Todos'] + list(df_filt['CONDUCTOR'].unique()))
if filtro_conductor != 'Todos':
    df_filt = df_filt[df_filt['CONDUCTOR'] == filtro_conductor]

filtro_estado = st.selectbox('Selecciona un estado:', ['Todos'] + list(df_filt['ESTADO'].unique()))
if filtro_estado != 'Todos':
    df_filt = df_filt[df_filt['ESTADO'] == filtro_estado]

# Mostrar datos filtrados si hay datos restantes
if not df_filt.empty:
    st.write("Datos filtrados:")
    st.write(df_filt)

    # Gráfico de barras para el recuento de vehículos
    fig_vehiculo = px.bar(df_filt['VEHICULO'].value_counts(), x=df_filt['VEHICULO'].value_counts().index, y=df_filt['VEHICULO'].value_counts().values, title='Recuento de Vehículos')
    st.plotly_chart(fig_vehiculo)

    # Gráfico de barras para el recuento de conductores
    fig_conductor = px.bar(df_filt['CONDUCTOR'].value_counts(), x=df_filt['CONDUCTOR'].value_counts().index, y=df_filt['CONDUCTOR'].value_counts().values, title='Recuento de Conductores')
    st.plotly_chart(fig_conductor)

    # Gráfico de barras para el recuento de estados
    fig_estado = px.bar(df_filt['ESTADO'].value_counts(), x=df_filt['ESTADO'].value_counts().index, y=df_filt['ESTADO'].value_counts().values, title='Recuento de Estados')
    st.plotly_chart(fig_estado)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
