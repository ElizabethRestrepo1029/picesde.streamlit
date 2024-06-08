import streamlit as st
import pandas as pd
import plotly.express as px

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
ruta_seleccionada = st.selectbox('Selecciona una ruta:', df['RUTA'].unique())
df_filtrado_ruta = df[df['RUTA'] == ruta_seleccionada]

# Filtro por conductor
conductor_seleccionado = st.selectbox('Selecciona un conductor:', df['CONDUCTOR'].unique())
df_filtrado_conductor = df[df['CONDUCTOR'] == conductor_seleccionado]

# Filtro por estado del viaje
estado_seleccionado = st.selectbox('Selecciona un estado:', df['ESTADO'].unique())
df_filtrado_estado = df[df['ESTADO'] == estado_seleccionado]

# Gráfico 1: Distribución de la diferencia entre el tiempo estimado y real de llegada
st.write("Distribución de la diferencia entre tiempo estimado y real de llegada:")
fig_hist = px.histogram(df, x='DIFERENCIA', nbins=10, title='Distribución de la diferencia')
st.plotly_chart(fig_hist)

# Gráfico 2: Cantidad de viajes por estado
st.write("Cantidad de viajes por estado:")
fig_bar_estado = px.bar(df['ESTADO'].value_counts(), x=df['ESTADO'].value_counts().index, y=df['ESTADO'].value_counts().values)
st.plotly_chart(fig_bar_estado)

# Gráfico 3: Tiempo promedio de llegada por ruta
st.write("Tiempo promedio de llegada por ruta:")
fig_bar_ruta = px.bar(df.groupby('RUTA')['DIFERENCIA'].mean(), x=df.groupby('RUTA')['DIFERENCIA'].mean().index, y=df.groupby('RUTA')['DIFERENCIA'].mean().values, title='Tiempo promedio de llegada por ruta')
st.plotly_chart(fig_bar_ruta)

# Gráfico 4: Tiempo promedio de llegada por conductor
st.write("Tiempo promedio de llegada por conductor:")
fig_bar_conductor = px.bar(df.groupby('CONDUCTOR')['DIFERENCIA'].mean(), x=df.groupby('CONDUCTOR')['DIFERENCIA'].mean().index, y=df.groupby('CONDUCTOR')['DIFERENCIA'].mean().values, title='Tiempo promedio de llegada por conductor')
st.plotly_chart(fig_bar_conductor)
