import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar el tema de Streamlit
st.set_page_config(
    page_title="Restaurante",
    page_icon=":fork_and_knife:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS para personalizar el estilo
st.markdown("""
    <style>
        .main {
            background-color: #B8CFE5;
            color: #02153B;
        }
        .stSelectbox label, .stButton button, .stSlider label, .stTextInput label {
            color: #02153B;
        }
        h1, h2, h3, h4 {
            color: #02153B;
        }
        .css-1ekf893 {
            background-color: #1f77b4;
        }
        .st-dx, .st-cn, .st-at {
            border: 2px solid #1f77b4;
            border-radius: 10px;
            padding: 10px;
        }
        header.css-18ni7ap {
            background-color: #0C1449;
        }
        header.css-18ni7ap .css-1v0mbdj, header.css-18ni7ap .css-1rs6os {
            color: #f0f2f6;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Restaurante")
st.markdown("""
    <h2 style='text-align: center; color: #02153B; font-size: 24px'>Donde encontrarás varios tipos de comidas</h2>
    <p style='text-align: center; font-size: px;'>🍖🍔🍹🍰</p>
""", unsafe_allow_html=True)

multi = '''***Es una aplicación para restaurante que permite la gestión integral de ventas.***

***El cual funciona conectando diferentes áreas como servicio (:red[meseros]), 
cocina (:red[chef]), facturación (:red[caja]) y (:red[administración]).***
'''
st.markdown(multi)

# Especificar la ruta del archivo CSV
file_path = 'static/Restaurante.csv'

# Intentar leer el archivo CSV con diferentes encodings
try:
    df = pd.read_csv(file_path, encoding='utf-8', sep=';')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1', sep=';')

# Asegurarse de que los nombres de las columnas no tengan espacios al principio o al final
df.columns = df.columns.str.strip()

# Convertir la columna 'Fecha' a datetime si existe
if 'Fecha' in df.columns:
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

# Filtrar las filas con fechas no convertibles
df = df.dropna(subset=['Fecha'])

# Extraer mes, día y hora de la columna 'Fecha'
df['Mes'] = df['Fecha'].dt.strftime('%Y-%m')
df['Dia'] = df['Fecha'].dt.date
df['Hora'] = df['Fecha'].dt.hour

# Obtener las opciones únicas de cada filtro
productosU = sorted(df['Producto'].unique())
usuariosU = sorted(df['Usuario'].unique()) if 'Usuario' in df.columns else []
diasU = sorted(df['Dia'].unique())
mesasU = sorted(df['Mesa'].unique())

# Configurar los selectores
optionProducto = st.selectbox('Producto', ['Todos'] + productosU)
optionUsuario = st.selectbox('Usuario', ['Todos'] + usuariosU) if usuariosU else None
optionFecha = st.date_input('Fecha', min_value=min(diasU), max_value=max(diasU), value=max(diasU))
optionMesa = st.selectbox('Mesa', ['Todos'] + mesasU)

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionProducto != "Todos":
    filtered_data = filtered_data[filtered_data['Producto'] == optionProducto]
if optionUsuario and optionUsuario != "Todos":
    filtered_data = filtered_data[filtered_data['Usuario'] == optionUsuario]
if optionFecha:
    filtered_data = filtered_data[filtered_data['Dia'] == optionFecha]
if optionMesa != "Todos":
    filtered_data = filtered_data[filtered_data['Mesa'] == optionMesa]

# Gráfico de barras para el total de ventas por producto
ventas_por_producto = filtered_data.groupby('Producto')['Total'].sum().reset_index()
fig_bar = px.bar(ventas_por_producto, x='Producto', y='Total', title='Total de Ventas por Producto')

# Gráfico de líneas para la evolución de ventas a lo largo del tiempo
ventas_por_fecha = filtered_data.groupby('Fecha')['Total'].sum().reset_index()
fig_line = px.line(ventas_por_fecha, x='Fecha', y='Total', title='Evolución de Ventas a lo Largo del Tiempo')

# Gráfico de picos para las ventas por mesa
if optionMesa != "Todos":
    ventas_por_mesa = filtered_data.groupby('Mesa')['Total'].sum().reset_index()
    fig_pie = px.pie(ventas_por_mesa, values='Total', names='Mesa', title='Ventas por Mesa')

# Gráfico de tortas para las ventas por producto
fig_torta = px.pie(ventas_por_producto, values='Total', names='Producto', title='Ventas por Producto')

# Gráfico de barras para las ventas por usuario
ventas_por_usuario = None
if optionUsuario and optionUsuario != "Todos":
    ventas_por_usuario = filtered_data.groupby('Usuario')['Total'].sum().reset_index()
    fig_bar_usuario = px.bar(ventas_por_usuario, x='Usuario', y='Total', title='Ventas por Usuario')

# Mostrar los gráficos
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)
if fig_bar_usuario is not None:
    st.plotly_chart(fig_bar_usuario, use_container_width=True)
if optionMesa != "Todos":
    st.plotly_chart(fig_pie, use_container_width=True)
st.plotly_chart(fig_torta, use_container_width=True)
