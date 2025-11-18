import pandas as pd
import streamlit as st

st.title("Análisis de Datos con Streamlit y Pandas")

CSV_PATH = 'static/Datos_netflix.csv'

try:
	# Probar distintas codificaciones comunes y elegir la que funcione
	df_netflix = None
	used_encoding = None
	for enc in ('utf-8', 'latin-1', 'cp1252'):
		try:
			df_netflix = pd.read_csv(CSV_PATH, sep=';', encoding=enc)
			used_encoding = enc
			break
		except Exception:
			continue

	if df_netflix is None:
		raise ValueError('No se pudo leer el CSV con las codificaciones probadas')

	st.success(f"Archivo cargado correctamente: {CSV_PATH} (encoding: {used_encoding})")
	st.write(f"Filas: {df_netflix.shape[0]}, Columnas: {df_netflix.shape[1]}")
	st.dataframe(df_netflix.head(10))
except FileNotFoundError:
	st.error(f"No se encontró el archivo: {CSV_PATH}")
except Exception as e:
	st.error(f"Error al leer el CSV: {e}")