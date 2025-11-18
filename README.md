# Proyecto de Análisis de Datos - Netflix

Este proyecto utiliza **Streamlit** y **Pandas** para el análisis y visualización de datos de Netflix.

## Configuración del Entorno de Desarrollo

### 1. Crear un Entorno Virtual

Primero, crea un entorno virtual para aislar las dependencias del proyecto. Abre una terminal (PowerShell) y ejecuta:

```powershell
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar Dependencias

Una vez activado el entorno virtual, instala todas las dependencias necesarias:

```powershell
pip install -r requirements.txt
```

Este comando instalará todas las bibliotecas requeridas, incluyendo:

- **streamlit** - framework web interactivo
- **pandas** - análisis y manipulación de datos
- **numpy** - computación numérica
- **matplotlib** y **seaborn** - visualización
- **mysql-connector-python** - conexión a bases de datos
- y otras dependencias necesarias

### 3. Ejecutar la Aplicación

Para iniciar la aplicación Streamlit localmente, ejecuta:

```powershell
streamlit run inicio.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado. Por defecto, la dirección será: `http://localhost:8501`

## Notas Importantes

- Asegúrate de tener **Python 3.8 o superior** instalado en tu sistema.
- El archivo CSV (`Datos_netflix.csv`) utiliza **`;` como separador** y **encoding `latin-1`**.
- Mantén el entorno virtual activado mientras trabajas en el proyecto.
- Si necesitas detener la aplicación, presiona `Ctrl+C` en la terminal.
- Para desactivar el entorno virtual cuando termines, ejecuta `deactivate` en la terminal.

## Estructura del Proyecto

```
proyecto1/
├── Inicio.py               # Aplicación principal de Streamlit (punto de entrada)
├── conexion_mysql.py       # Configuración de conexión a MySQL
├── requirements.txt        # Lista de dependencias del proyecto
├── .env                    # Variables de entorno
├── README.md               # Este archivo
├── pages/
│   ├── base_de_datos.py    # Módulo para gestionar datos de base de datos
│   └── datos_csv.py        # Módulo para gestionar datos CSV
├── static/
│   └── Datos_netflix.csv   # Dataset principal (separador: `;`, encoding: `latin-1`)
└── assets/
    └── netflis.png         # Recurso de imagen
```

## Archivos Principales

- **`Inicio.py`**: Aplicación Streamlit que carga y visualiza los datos de Netflix en una tabla interactiva.
- **`conexion_mysql.py`**: Módulo para gestionar conexiones a bases de datos MySQL.
- **`pages/base_de_datos.py`**: Módulo para gestionar operaciones con la base de datos.
- **`pages/datos_csv.py`**: Módulo para gestionar operaciones con archivos CSV.
- **`static/Datos_netflix.csv`**: Dataset con información de sesiones, usuarios, películas y series de Netflix.
