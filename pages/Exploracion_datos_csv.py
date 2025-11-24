import pandas as pd
import streamlit as st
from io import StringIO

st.title("Análisis de Datos con Streamlit y Pandas")

RUTA_CSV = 'static/Datos_netflix.csv'

try:
	# Probar distintas codificaciones comunes y elegir la que funcione
	df_netflix = None
	codificacion_usada = None
	for codificacion in ('utf-8', 'latin-1', 'cp1252'):
		try:
			df_netflix = pd.read_csv(RUTA_CSV, sep=';', encoding=codificacion)
			codificacion_usada = codificacion
			break
		except Exception:
			continue

	if df_netflix is None:
		raise ValueError('No se pudo leer el CSV con las codificaciones probadas')

	st.success(f"Archivo cargado correctamente: {RUTA_CSV} (encoding: {codificacion_usada})")
	st.write(f"Filas: {df_netflix.shape[0]}, Columnas: {df_netflix.shape[1]}")



	st.header("Exploración de múltiples archivos CSV")
	subtabs = st.tabs(["Primeros 10 registros", "Últimos 10 registros", "Información", "Descripción"])

	with subtabs[0]:
		codigo = """
		st.subheader('Primeros 10 registros')
		st.dataframe(df_netflix.head(10))
		"""
		st.subheader('Primeros 10 registros')
		st.code(codigo, language='python')
		st.dataframe(df_netflix.head(10))

	with subtabs[1]:
		codigo = """
		st.subheader('Últimos 10 registros')
		st.dataframe(df_netflix.tail(10))
		"""
		st.subheader('Últimos 10 registros')
		st.code(codigo, language='python')
		st.dataframe(df_netflix.tail(10))

	with subtabs[2]:
		code = """
		st.subheader('Información del DataFrame')
		buffer = StringIO()
		df_netflix.info(buf=buffer)
		info_text = buffer.getvalue()
		st.text(info_text)
		"""
		st.subheader('Información del DataFrame')
		st.code(code, language='python')
		buffer = StringIO()
		df_netflix.info(buf=buffer)
		info_text = buffer.getvalue()
		st.text(info_text)

	with subtabs[3]:
		codigo = """
		st.subheader('Descripción estadística del DataFrame')
		st.dataframe(df_netflix.describe(include='all').T)
		"""
		st.subheader('Descripción estadística del DataFrame')
		st.code(codigo,language='python')
		st.dataframe(df_netflix.describe(include='all').T)

	st.header('Porcentaje de progreso por usuario ')
	if ('porcentaje_progreso' in df_netflix.columns and 'id_usuario' in df_netflix.columns) and 'titulo' in df_netflix.columns:
		# Agrupar calculando la media de porcentaje_progreso y conservando títulos (lista corta de únicos)
		progreso_por_usuario = df_netflix.groupby('id_usuario').agg({
			'porcentaje_progreso': 'mean',
			'titulo': lambda x: ', '.join(x.dropna().astype(str).unique()[:3])
		}).reset_index()
		progreso_por_usuario['porcentaje_progreso'] = progreso_por_usuario['porcentaje_progreso'].round(2)
		
		# Filtrar solo registros con porcentaje_progreso mayor a 60
		filtro = progreso_por_usuario[progreso_por_usuario['porcentaje_progreso'] > 60]

		codigo = """
		st.header('Porcentaje de progreso por usuario ')
		if 'porcentaje_progreso' in df_netflix.columns and 'id_usuario' in df_netflix.columns and 'titulo' in df_netflix.columns:
			progreso_por_usuario = df_netflix.groupby('id_usuario').agg({
				'porcentaje_progreso': 'mean',
				'titulo': lambda x: ', '.join(x.dropna().astype(str).unique()[:3])
			}).reset_index()
			progreso_por_usuario['porcentaje_progreso'] = progreso_por_usuario['porcentaje_progreso'].round(2)
			filtro = progreso_por_usuario[progreso_por_usuario['porcentaje_progreso'] > 60]
			st.dataframe(filtro.head(15))
		"""
		st.code(codigo, language='python')
		st.dataframe(filtro.head(15))
	else:
		st.warning("Las columnas 'porcentaje_progreso','id_usuario' y 'titulo' no están presentes en el DataFrame.")
	
except FileNotFoundError:
	st.error(f"No se encontró el archivo: {RUTA_CSV}")
except Exception as error:
	st.error(f"Error al leer el CSV: {error}")