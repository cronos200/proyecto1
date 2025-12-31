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

		# 1. Configurar estilo visual para la gráfica (fondo blanco con rejilla)
		sbn.set_style("whitegrid")
		# 2. Crear figura y ejes (tamaño para que las etiquetas sean legibles)
		fig, ax = plt.subplots(figsize=(12, 6))
		# 3. Seleccionar los mejores usuarios (top 20 por porcentaje promedio)
		top_20 = filtro.nlargest(20, 'porcentaje_progreso')
		# Manejar el caso en que no hay datos suficientes para graficar
		if top_20.empty:
			st.info("No hay usuarios con porcentaje de progreso > 60% para mostrar el gráfico.")
		else:
			# 4. Crear el gráfico de barras con seaborn
			sbn.barplot(
    			data=top_20,                    # DataFrame a usar
    			x='id_usuario',                 # Eje X: IDs de usuarios
    			y='porcentaje_progreso',        # Eje Y: Porcentaje
    			palette='viridis',              # Paleta de colores (azul-verde-amarillo)
    			ax=ax                           # Ejes donde dibujar
			)
			# 5. Añadir línea de referencia (umbral), título y etiquetas
			ax.axhline(y=60, color='red', linestyle='--', linewidth=2,
				label='Umbral 60%', alpha=0.7)
			ax.set_title("Top usuarios por porcentaje de progreso (media por usuario)")
			ax.set_xlabel("ID de usuario")
			ax.set_ylabel("Porcentaje de progreso (%)")
			ax.legend()
			# 6. Ajustar diseño: rotar etiquetas y ajustar layout
			plt.xticks(rotation=45, ha='right')  # Rotar etiquetas 45° a la derecha
			plt.tight_layout()                   # Ajustar para que no se corten elementos
			# 7. Mostrar la figura en Streamlit y cerrar la figura para liberar memoria
			st.pyplot(fig)
			plt.close(fig)
			# 8. Explicación breve en la interfaz sobre cómo se construyó la visualización
			st.caption("Gráfico de barras: se agruparon los registros por `id_usuario`, se calculó la media de `porcentaje_progreso` y se mostraron los 20 usuarios con mayor promedio (solo usuarios con promedio > 60%). La línea roja indica el umbral del 60%.")
	else:
		st.warning("Las columnas 'porcentaje_progreso','id_usuario' y 'titulo' no están presentes en el DataFrame.")
	

except FileNotFoundError:
	st.error(f"No se encontró el archivo: {RUTA_CSV}")
except Exception as error:
	st.error(f"Error al leer el CSV: {error}")