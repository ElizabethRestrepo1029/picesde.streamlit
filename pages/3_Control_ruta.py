import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurar el tema de Streamlit
st.set_page_config(
    page_title="Simulador Cesde",
    page_icon=":fork_and_knife:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS para personalizar el estilo
st.markdown("""
    <style>
        .main {
            background-color: #000000;
            color: #FFD700;
        }
        .stSelectbox label, .stButton button, .stSlider label, .stTextInput label {
            color: #FFD700;
        }
        h1, h2, h3, h4 {
            color: #FFD700;
        }
        .css-1ekf893 {
            background-color: #A60D0D;
        }
        .st-dx, .st-cn, .st-at {
            border: 2px solid #A60D0D;
            border-radius: 10px;
            padding: 10px;
        }
        header.css-18ni7ap {
            background-color: #A60D0D;
        }
        header.css-18ni7ap .css-1v0mbdj, header.css-18ni7ap .css-1rs6os {
            color: #FFD700;
        }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.title("Simulador Cesde")

# Leer el archivo CSV con manejo de errores de codificación
try:
    df = pd.read_csv('static/controlruta.csv', encoding='latin1')
except UnicodeDecodeError:
    st.error("Error de decodificación con la codificación 'latin1'. Intentando con 'utf-8'.")
    try:
        df = pd.read_csv('static/controlruta.csv', encoding='utf-8')
    except UnicodeDecodeError:
        st.error("Error de decodificación con la codificación 'utf-8'. Asegúrate de que el archivo CSV tenga una codificación compatible.")
        st.stop()
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()

# Filtrar las filas con horas no convertibles
df = df.dropna(subset=['HORA DE INICIO', 'HORA ESTIMADA DE LLEGADA', 'HORA REAL DE LLEGADA'])

# Convertir las columnas de hora a datetime
df['HORA DE INICIO'] = pd.to_datetime(df['HORA DE INICIO'], format='%I:%M:%S %p', errors='coerce')
df['HORA ESTIMADA DE LLEGADA'] = pd.to_datetime(df['HORA ESTIMADA DE LLEGADA'], format='%I:%M:%S %p', errors='coerce')
df['HORA REAL DE LLEGADA'] = pd.to_datetime(df['HORA REAL DE LLEGADA'], format='%I:%M:%S %p', errors='coerce')

# Extraer mes, día y hora de la columna 'HORA DE INICIO'
df['Mes'] = df['FECHA'].dt.strftime('%Y-%m')
df['Dia'] = df['FECHA'].dt.date
df['Hora'] = df['FECHA'].dt.hour

# Obtener las opciones únicas de cada filtro
vehiculosU = sorted(df['VEHICULO'].unique())
conductoresU = sorted(df['CONDUCTOR'].unique())
diasU = sorted(df['Dia'].unique())
estadosU = sorted(df['ESTADO'].unique())

# Configurar los selectores en cuatro columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    optionVehiculo = st.selectbox('Vehículo', ['Todos'] + vehiculosU)

with col2:
    optionConductor = st.selectbox('Conductor', ['Todos'] + conductoresU)

with col3:
    optionFecha = st.date_input('Fecha', min_value=min(diasU), max_value=max(diasU), value=max(diasU))

with col4:
    optionEstado = st.selectbox('Estado', ['Todos'] + estadosU)

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionVehiculo != "Todos":
    filtered_data = filtered_data[filtered_data['VEHICULO'] == optionVehiculo]
if optionConductor != "Todos":
    filtered_data = filtered_data[filtered_data['CONDUCTOR'] == optionConductor]
if optionFecha:
    filtered_data = filtered_data[filtered_data['Dia'] == optionFecha]
if optionEstado != "Todos":
    filtered_data = filtered_data[filtered_data['ESTADO'] == optionEstado]

# Gráficos
# Gráfico de barras para el número de viajes por vehículo
viajes_por_vehiculo = filtered_data.groupby('VEHICULO').size().reset_index(name='Count')
fig_bar_vehiculo = px.bar(viajes_por_vehiculo, x='VEHICULO', y='Count', title='Número de Viajes por Vehículo')

# Gráfico de barras para el número de viajes por conductor
viajes_por_conductor = filtered_data.groupby('CONDUCTOR').size().reset_index(name='Count')
fig_bar_conductor = px.bar(viajes_por_conductor, x='CONDUCTOR', y='Count', title='Número de Viajes por Conductor')

# Gráfico de líneas para la evolución de llegadas a lo largo del tiempo
llegadas_por_fecha = filtered_data.groupby('HORA DE INICIO')['DIFERENCIA'].sum().reset_index()
fig_line = px.line(llegadas_por_fecha, x='HORA DE INICIO', y='DIFERENCIA', title='Evolución de Diferencia de Llegadas a lo Largo del Tiempo')

# Gráfico de barras para el número de viajes por estado
viajes_por_estado = filtered_data.groupby('ESTADO').size().reset_index(name='Count')
fig_bar_estado = px.bar(viajes_por_estado, x='ESTADO', y='Count', title='Número de Viajes por Estado')

# Mostrar los gráficos
st.plotly_chart(fig_bar_vehiculo, use_container_width=True)
st.plotly_chart(fig_bar_conductor, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)
st.plotly_chart(fig_bar_estado, use_container_width=True)
