import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Proyecto Integrador - Ventas Restaurante")

# Especificar la ruta del archivo CSV
file_path = 'static/Restaurante.csv'

# Intentar leer el archivo CSV con diferentes encodings
try:
    df = pd.read_csv(file_path, encoding='utf-8', sep=';')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1', sep=';')

# Asegurarse de que los nombres de las columnas no tengan espacios al principio o al final
df.columns = df.columns.str.strip()

# Verificar si la columna 'Fecha' existe en el DataFrame
if 'Fecha' not in df.columns:
    st.error("La columna 'Fecha' no se encontró en el archivo de datos. Asegúrate de que el archivo CSV tenga la columna 'Fecha'.")
    st.stop()

# Convertir la columna 'Fecha' a datetime y separar la hora si está en la misma columna
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

# Si la hora está en una columna separada, convertirla a formato datetime y combinarla con la fecha
if 'Hora' in df.columns:
    df['Hora'] = pd.to_datetime(df['Hora'], format='%I:%M:%S %p', errors='coerce').dt.time
    df['Fecha_Hora'] = df.apply(lambda row: pd.datetime.combine(row['Fecha'], row['Hora']), axis=1)
else:
    df['Fecha_Hora'] = df['Fecha']

# Filtrar las filas con fechas no convertibles
df = df.dropna(subset=['Fecha_Hora'])

# Extraer mes, día y hora de la columna 'Fecha_Hora'
df['Mes'] = df['Fecha_Hora'].dt.to_period('M')
df['Dia'] = df['Fecha_Hora'].dt.date
df['Hora'] = df['Fecha_Hora'].dt.hour

# Obtener las opciones únicas de cada filtro
productosU = sorted(df['Producto'].unique())
mesesU = sorted(df['Mes'].unique().astype(str))
diasU = sorted(df['Dia'].unique())
# Configurar las columnas y selectores
col1, col2 = st.columns(2)

with col1:
    mesesU.insert(0, "Todos")
    optionMes = st.selectbox('Mes', (mesesU))

with col2:
    productosU.insert(0, "Todos")
    optionProducto = st.selectbox('Producto', (productosU))

col3, col4 = st.columns(2)

with col3:
    diasU.insert(0, "Todos")
    optionDia = st.selectbox('Día', (diasU))

with col4:
    optionHora = st.slider('Rango de Hora', min_value=0, max_value=23, value=(0, 23))

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionMes != "Todos":
    filtered_data = filtered_data[filtered_data['Mes'].astype(str) == optionMes]

if optionProducto != "Todos":
    filtered_data = filtered_data[filtered_data['Producto'] == optionProducto]

if optionDia != "Todos":
    filtered_data = filtered_data[filtered_data['Dia'] == optionDia]

start_hour, end_hour = optionHora
filtered_data = filtered_data[(filtered_data['Hora'] >= start_hour) & (filtered_data['Hora'] <= end_hour)]

# Crear un gráfico de barras horizontales para el total de ventas por producto
ventas_por_producto = filtered_data.groupby('Producto')['Total'].sum().reset_index()
fig_bar_horizontal = px.bar(ventas_por_producto, x='Total', y='Producto', orientation='h', title='Total de Ventas por Producto (Horizontal)')

# Crear un gráfico de líneas para la evolución de ventas en el tiempo
ventas_por_fecha = filtered_data.groupby('Fecha')['Total'].sum().reset_index()
fig_line = px.line(ventas_por_fecha, x='Fecha', y='Total', title='Evolución de Ventas a lo Largo del Tiempo')

# Crear un gráfico de barras para las ventas por hora
ventas_por_hora = filtered_data.groupby('Hora')['Total'].sum().reset_index()
fig_bar_hora = px.bar(ventas_por_hora, x='Hora', y='Total', title='Ventas por Hora del Día')

# Crear un gráfico de barras vertical para las ventas por día
ventas_por_dia = filtered_data.groupby('Dia')['Total'].sum().reset_index()
fig_bar_dia = px.bar(ventas_por_dia, x='Dia', y='Total', title='Ventas por Día', orientation='v')

# Crear un gráfico circular (de torta) para la proporción de ventas por producto
fig_pie = px.pie(ventas_por_producto, values='Total', names='Producto', title='Proporción de Ventas por Producto')

# Mostrar los gráficos
st.plotly_chart(fig_bar_horizontal, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)
st.plotly_chart(fig_bar_hora, use_container_width=True)
st.plotly_chart(fig_bar_dia, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)

# Mostrar la tabla filtrada
st.write("Datos filtrados", filtered_data)
