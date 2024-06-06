import streamlit as st
import pandas as pd
import plotly.figure_factory as ff

import plotly.graph_objects as go

st.write("Proyecto integrador")
try:
    df = pd.read_csv('static/Restaurante.csv')
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()