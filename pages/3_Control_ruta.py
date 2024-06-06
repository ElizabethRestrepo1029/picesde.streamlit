import streamlit as st
import pandas as pd
import plotly.figure_factory as ff

import plotly.graph_objects as go

st.write("Control de rutas")
try:
    df = pd.read_csv('static/controlrutas.csv')
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()