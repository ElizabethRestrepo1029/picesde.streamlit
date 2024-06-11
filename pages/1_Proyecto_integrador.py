import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Restaurante")
st.markdown(" ***:rainbow[Donde encontraras varios tipos de comidas]***; :meat_on_bone::hamburger::tropical_drink::cake:")

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

# Verificar si la columna 'Hora' existe en el DataFrame
if 'Hora' not in df.columns:
    st.error("La columna 'Hora' no se encontró en el archivo de datos. Asegúrate de que el archivo CSV tenga la columna 'Hora'.")
    st.stop()
# Obtener las opciones únicas de cada filtro
productosU = sorted(df['Producto'].unique())
meserosU = sorted(df['Mesero'].unique()) if 'Mesero' in df.columns else []
mesesU = sorted(df['Mes'].unique())
diasU = sorted(df['Dia'].unique())
diasSemanaU = sorted(df['DiaSemana'].unique())
horasU = [str(h) + ":00" for h in range(12, 24)]

# Configurar los selectores
optionProducto = st.selectbox('Producto', ['Todos'] + productosU)
optionMesero = st.selectbox('Mesero', ['Todos'] + meserosU) if meserosU else 'Todos'
optionMes = st.selectbox('Mes', ['Todos'] + mesesU)
optionDia = st.selectbox('Día', ['Todos'] + diasU)
optionDiaSemana = st.selectbox('Día de la Semana', ['Todos'] + diasSemanaU)
optionHora = st.selectbox('Hora', ['Todos'] + horasU)

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
if optionHora != "Todos":
    hour = int(optionHora.split(":")[0])
    filtered_data = filtered_data[filtered_data['Hora'] == hour]

# Gráficos
def plot_graph(data, x, y, title):
    fig = px.bar(data, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)

plot_graph(filtered_data.groupby('Producto')['Total'].sum().reset_index(), 'Producto', 'Total', 'Total de Ventas por Producto')
plot_graph(filtered_data.groupby('Fecha')['Total'].sum().reset_index(), 'Fecha', 'Total', 'Evolución de Ventas a lo Largo del Tiempo')
plot_graph(filtered_data.groupby('Hora')['Total'].sum().reset_index(), 'Hora', 'Total', 'Ventas por Hora')
plot_graph(filtered_data.groupby('DiaSemana')['Total'].sum().reset_index(), 'DiaSemana', 'Total', 'Distribución de Ventas por Día de la Semana')
if 'Mesero' in df.columns:
    plot_graph(filtered_data.groupby('Mesero')['Total'].sum().reset_index(), 'Mesero', 'Total', 'Total de Ventas por Mesero')
