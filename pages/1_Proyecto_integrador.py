import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.write("Proyecto integrador")
try:
    df = pd.read_csv('static\Restaurante.csv')
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()

# Convertir la columna de fecha a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Filtro por mesa
def filtro_mesa(mesa):
    return df[df['Mesa'] == mesa]

# Filtro por usuario
def filtro_usuario(usuario):
    return df[df['Usuario'] == usuario]

# Filtro por estado
def filtro_estado(estado):
    return df[df['Estado'] == estado]

# Filtro por producto
def filtro_producto(producto):
    return df[df['Producto'] == producto]

# Gráfico 1: Distribución de ventas por estado
plt.figure(figsize=(8, 6))
df['Estado'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Distribución de ventas por estado')
plt.axis('equal')
plt.show()

# Gráfico 2: Top 5 productos más vendidos
top_productos = df.groupby('Producto')['Cantidad'].sum().nlargest(5)
plt.figure(figsize=(10, 6))
top_productos.plot(kind='bar', color='skyblue')
plt.xlabel('Producto')
plt.ylabel('Cantidad vendida')
plt.title('Top 5 productos más vendidos')
plt.xticks(rotation=45)
plt.show()

# Gráfico 3: Total de ventas por usuario
ventas_por_usuario = df.groupby('Usuario')['Total'].sum()
plt.figure(figsize=(10, 6))
ventas_por_usuario.plot(kind='bar', color='salmon')
plt.xlabel('Usuario')
plt.ylabel('Total de ventas')
plt.title('Total de ventas por usuario')
plt.xticks(rotation=45)
plt.show()

# Gráfico 4: Total de ventas por día
ventas_por_dia = df.groupby(df['Fecha'].dt.date)['Total'].sum()
plt.figure(figsize=(10, 6))
ventas_por_dia.plot(kind='line', marker='o', color='green')
plt.xlabel('Fecha')
plt.ylabel('Total de ventas')
plt.title('Total de ventas por día')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
