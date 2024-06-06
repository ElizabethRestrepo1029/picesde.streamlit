import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.write("Control de rutas")
try:
    df = pd.read_csv('static\controlrutas.csv')
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()


# Convertir las columnas de fecha a tipo datetime
df['HORA DE INICIO'] = pd.to_datetime(df['HORA DE INICIO'])
df['HORA ESTIMADA DE LLEGADA'] = pd.to_datetime(df['HORA ESTIMADA DE LLEGADA'])
df['HORA REAL DE LLEGADA'] = pd.to_datetime(df['HORA REAL DE LLEGADA'])

# Filtro por ruta
def filtro_ruta(ruta):
    return df[df['RUTA'] == ruta]

# Filtro por conductor
def filtro_conductor(conductor):
    return df[df['CONDUCTOR'] == conductor]

# Filtro por estado del viaje
def filtro_estado(estado):
    return df[df['ESTADO'] == estado]

# Gráfico 1: Distribución de la diferencia entre el tiempo estimado y real de llegada
plt.figure(figsize=(10, 6))
plt.hist(df['DIFERENCIA'], bins=10, color='skyblue', edgecolor='black')
plt.xlabel('Diferencia (minutos)')
plt.ylabel('Cantidad de viajes')
plt.title('Distribución de la diferencia entre tiempo estimado y real de llegada')
plt.grid(True)
plt.show()

# Gráfico 2: Cantidad de viajes por estado
plt.figure(figsize=(8, 6))
df['ESTADO'].value_counts().plot(kind='bar', color='salmon')
plt.xlabel('Estado del viaje')
plt.ylabel('Cantidad de viajes')
plt.title('Cantidad de viajes por estado')
plt.xticks(rotation=45)
plt.show()

# Gráfico 3: Tiempo promedio de llegada por ruta
plt.figure(figsize=(10, 6))
df.groupby('RUTA')['DIFERENCIA'].mean().plot(kind='bar', color='lightgreen')
plt.xlabel('Ruta')
plt.ylabel('Tiempo promedio de llegada (minutos)')
plt.title('Tiempo promedio de llegada por ruta')
plt.xticks(rotation=45)
plt.show()

# Gráfico 4: Tiempo promedio de llegada por conductor
plt.figure(figsize=(10, 6))
df.groupby('CONDUCTOR')['DIFERENCIA'].mean().plot(kind='bar', color='orange')
plt.xlabel('Conductor')
plt.ylabel('Tiempo promedio de llegada (minutos)')
plt.title('Tiempo promedio de llegada por conductor')
plt.xticks(rotation=45)
plt.show()
