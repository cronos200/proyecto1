# Proyecto de Análisis de Datos

Este proyecto utiliza Streamlit para la visualización de datos y MySQL como base de datos.

## Configuración del Entorno de Desarrollo

### 1. Crear un Entorno Virtual

Primero, crea un entorno virtual para aislar las dependencias del proyecto. Abre una terminal y ejecuta:

```powershell
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual
.\venv\Scripts\activate
```

### 2. Instalar Dependencias

Una vez activado el entorno virtual, instala todas las dependencias necesarias:

```powershell
pip install -r requirements.txt
```

Este comando instalará todas las bibliotecas requeridas, incluyendo:

- streamlit
- mysql-connector-python
- pandas
- numpy
- matplotlib
- seaborn
- y otras dependencias necesarias

### 3. Ejecutar la Aplicación

Para iniciar la aplicación Streamlit localmente, ejecuta:

```powershell
streamlit run app_streamlit.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado. Por defecto, la dirección será: `http://localhost:8501`

## Notas Importantes

- Asegúrate de tener Python 3.8 o superior instalado en tu sistema.
- Mantén el entorno virtual activado mientras trabajas en el proyecto.
- Si necesitas detener la aplicación, presiona `Ctrl+C` en la terminal.
- Para desactivar el entorno virtual cuando termines, simplemente ejecuta `deactivate` en la terminal.

## Estructura del Proyecto

```
Proyecto1/
├── app_streamlit.py      # Aplicación principal de Streamlit
├── conexion_mysql.py     # Configuración de conexión a MySQL
├── inicio.py            # Archivo de inicio
├── requirements.txt     # Lista de dependencias
├── data/               # Directorio para datos
└── scripts/            # Directorio para scripts adicionales
```
