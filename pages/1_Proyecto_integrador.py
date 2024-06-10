import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("*Proyecto * Integrador **-**Ventas** ***Restaurante***.")
st.markdown('''
    :red[Ventas] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[Restaurante] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Donde encontraras varios tipos de comidas; :meat_on_bone::hamburger::tropical_drink::cake:")


multi = '''Es una aplicación para restaurante que permite la gestión integral de ventas.

El cual funciona conectando diferentes áreas como servicio (meseros), 
cocina (chef), facturación (caja) y administración
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

# Verificar si la columna 'Fecha' existe en el DataFrame
if 'Fecha' not in df.columns:
    st.error("La columna 'Fecha' no se encontró en el archivo de datos. Asegúrate de que el archivo CSV tenga la columna 'Fecha'.")
    st.stop()

# Convertir la columna 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y %H:%M', errors='coerce')

# Filtrar las filas con fechas no convertibles
df = df.dropna(subset=['Fecha'])

# Extraer mes, día y hora de la columna 'Fecha'
df['Mes'] = df['Fecha'].dt.strftime('%Y-%m')
df['Dia'] = df['Fecha'].dt.date
df['Hora'] = df['Fecha'].dt.hour
df['DiaSemana'] = df['Fecha'].dt.day_name()

# Obtener las opciones únicas de cada filtro
productosU = sorted(df['Producto'].unique())
meserosU = sorted(df['Mesero'].unique()) if 'Mesero' in df.columns else []
mesesU = sorted(df['Mes'].unique())
diasU = sorted(df['Dia'].unique())
diasSemanaU = sorted(df['DiaSemana'].unique())

# Configurar los selectores
optionProducto = st.selectbox('Producto', ['Todos'] + productosU)
optionMesero = st.selectbox('Mesero', ['Todos'] + meserosU) if meserosU else 'Todos'
optionMes = st.selectbox('Mes', ['Todos'] + mesesU)
optionDia = st.selectbox('Día', ['Todos'] + diasU)
optionDiaSemana = st.selectbox('Día de la Semana', ['Todos'] + diasSemanaU)

# Filtro de hora con formato de 12 horas (AM/PM)
optionHoraInicio = st.slider('Hora de Inicio', 12, 23, 12)
optionHoraFin = st.slider('Hora de Fin', 12, 23, 23)

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionProducto != "Todos":
    filtered_data = filtered_data[filtered_data['Producto'] == optionProducto]
if optionMesero != "Todos" and 'Mesero' in df.columns:
    filtered_data = filtered_data[filtered_data['Mesero'] == optionMesero]
if optionMes != "Todos":
    filtered_data = filtered_data[filtered_data['Mes'] == optionMes]
if optionDia != "Todos":
    filtered_data = filtered_data[filtered_data['Dia'] == optionDia]
if optionDiaSemana != "Todos":
    filtered_data = filtered_data[filtered_data['DiaSemana'] == optionDiaSemana]

# Filtrar por rango de hora
filtered_data = filtered_data[(filtered_data['Hora'] >= optionHoraInicio) & (filtered_data['Hora'] <= optionHoraFin)]

# Gráfico de barras para el total de ventas por producto
ventas_por_producto = filtered_data.groupby('Producto')['Total'].sum().reset_index()
fig_bar_producto = px.bar(ventas_por_producto, x='Producto', y='Total', title='Total de Ventas por Producto')

# Gráfico de líneas para la evolución de ventas a lo largo del tiempo
ventas_por_fecha = filtered_data.groupby('Fecha')['Total'].sum().reset_index()
fig_line_fecha = px.line(ventas_por_fecha, x='Fecha', y='Total', title='Evolución de Ventas a lo Largo del Tiempo')

# Gráfico de barras para las ventas por hora
ventas_por_hora = filtered_data.groupby('Hora')['Total'].sum().reset_index()
fig_bar_hora = px.bar(ventas_por_hora, x='Hora', y='Total', title='Ventas por Hora')

# Gráfico de pastel para la distribución de ventas por día de la semana
ventas_por_dia_semana = filtered_data.groupby('DiaSemana')['Total'].sum().reset_index()
fig_pie_dia_semana = px.pie(ventas_por_dia_semana, values='Total', names='DiaSemana', title='Distribución de Ventas por Día de la Semana')

# Gráfico de barras para el total de ventas por mesero
ventas_por_mesero = filtered_data.groupby('Mesero')['Total'].sum().reset_index() if 'Mesero' in df.columns else None
fig_bar_mesero = px.bar(ventas_por_mesero, x='Mesero', y='Total', title='Total de Ventas por Mesero') if ventas_por_mesero is not None else None

# Mostrar los gráficos
st.plotly_chart(fig_bar_producto, use_container_width=True)
st.plotly_chart(fig_line_fecha, use_container_width=True)
st.plotly_chart(fig_bar_hora, use_container_width=True)
st.plotly_chart(fig_pie_dia_semana, use_container_width=True)
if fig_bar_mesero:
    st.plotly_chart(fig_bar_mesero, use_container_width=True)
