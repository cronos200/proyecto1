import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sbn
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



	st.header("Exploración del archivo Datos_netflix.csv")
	subtabs = st.tabs(["Primeros 30 registros", "Últimos 30 registros", "Información", "Descripción"])

	with subtabs[0]:
		codigo = """
		st.subheader('Primeros 30 registros')
		st.dataframe(df_netflix.head(30))
		"""
		st.subheader('Primeros 30 registros')
		st.code(codigo, language='python')
		st.dataframe(df_netflix.head(30))

	with subtabs[1]:
		codigo = """
		st.subheader('Últimos 30 registros')
		st.dataframe(df_netflix.tail(30))
		"""
		st.subheader('Últimos 30 registros')
		st.code(codigo, language='python')
		st.dataframe(df_netflix.tail(30))

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

		# --- INICIO DE LÍNEAS MODIFICADAS ---
		
		# 1. Configurar estilo visual general
		sbn.set_style("whitegrid")
		st.divider()

		# Creamos dos columnas para mostrar gráficas complementarias
		grfica1, grafica2 = st.columns(2)

		with grfica1:
			st.subheader("Distribución del Compromiso")
			# Histograma: Permite ver si la mayoría de usuarios termina lo que ve o lo deja al inicio
			fig_dist, ax_dist = plt.subplots(figsize=(8, 5))
			sbn.histplot(df_netflix['porcentaje_progreso'], bins=20, kde=True, color='teal', ax=ax_dist)
			ax_dist.set_title("Frecuencia de avance en los títulos")
			ax_dist.set_xlabel("Porcentaje de Progreso (%)")
			ax_dist.set_ylabel("Cantidad de Visualizaciones")
			st.pyplot(fig_dist)
			plt.close(fig_dist)
			st.caption("Esta gráfica muestra la distribución del progreso. Ayuda a identificar si el comportamiento común es ver el contenido completo o abandonarlo pronto.")

		with grafica2:
			st.subheader("Progreso Medio por Género")
			# Gráfico de Barras por Categoría: Útil para saber qué géneros mantienen más tiempo al usuario
			if 'genero_principal' in df_netflix.columns:
				progreso_gen = df_netflix.groupby('genero_principal')['porcentaje_progreso'].mean().sort_values(ascending=False).reset_index()
				fig_gen, ax_gen = plt.subplots(figsize=(8, 5))
				sbn.barplot(data=progreso_gen, x='porcentaje_progreso', y='genero_principal', palette='viridis', ax=ax_gen)
				ax_gen.set_title("Géneros con mayor retención")
				ax_gen.set_xlabel("Progreso Promedio (%)")
				ax_gen.set_ylabel("Género Principal")
				st.pyplot(fig_gen)
				plt.close(fig_gen)
				st.caption("Se comparan los géneros según el porcentaje medio que los usuarios consumen antes de cerrar la sesión.")

		# Visualización de Dispositivos (Opcional, muy acorde a los datos)
		st.subheader("Análisis de consumo por Dispositivo")
		if 'tipo_dispositivo' in df_netflix.columns:
			fig_dev, ax_dev = plt.subplots(figsize=(10, 4))
			sbn.boxplot(data=df_netflix, x='tipo_dispositivo', y='porcentaje_progreso', palette='Set2', ax=ax_dev)
			ax_dev.set_title("Dispersión del progreso según el dispositivo utilizado")
			ax_dev.set_xlabel("Dispositivo")
			ax_dev.set_ylabel("Progreso (%)")
			st.pyplot(fig_dev)
			plt.close(fig_dev)
			st.caption("El diagrama de caja (Boxplot) permite ver no solo el promedio, sino la variabilidad del progreso en diferentes dispositivos (Tablet, Smart TV, etc.).")

		# --- FIN DE LÍNEAS MODIFICADAS ---
		st.warning("Las columnas 'porcentaje_progreso','id_usuario' y 'titulo' no están presentes en el DataFrame.")
	

except FileNotFoundError:
	st.error(f"No se encontró el archivo: {RUTA_CSV}")
except Exception as error:
	st.error(f"Error al leer el CSV: {error}")