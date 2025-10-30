# Conexión segura a MySQL con SQLAlchemy y dotenv
# ----------------------------------------
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

# 1️⃣ Cargar las variables del archivo .env
load_dotenv()

USUARIO = os.getenv("DB_USUARIO")
CONTRASENA = os.getenv("DB_CONTRASENA")
HOST = os.getenv("DB_HOST")
PUERTO = os.getenv("DB_PUERTO")
NOMBRE = os.getenv("DB_NOMBRE")

# 2️⃣ Crear la URL de conexión
# formato general:
# mysql+pymysql://usuario:contraseña@host:puerto/base_datos
connection_url = f"mysql+pymysql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{NOMBRE}"

# El bloque try-except se utiliza para manejar errores de forma segura:
# - try: Intenta ejecutar el código que podría generar un error
# - except: Captura y maneja el error si ocurre, evitando que el programa se detenga
# En este caso, intentamos crear una conexión a la base de datos y si falla,
# mostraremos un mensaje de error en lugar de crashear el programa
# 3️⃣ Crear el motor de conexión
try:
    engine = create_engine(connection_url)
    print("✅ Conexión a la base de datos exitosa")

except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)

# 4️⃣ Probar la conexión ejecutando una consulta simple
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) AS total_registros FROM ventas"))
        total = result.scalar()
        print(f"📊 Total de registros en la tabla 'ventas': {total}")

except Exception as e:
    print("⚠️ Error al ejecutar la consulta:", e)

# 5️⃣ Leer los datos en un DataFrame de pandas
try:
    df = pd.read_sql("SELECT * FROM ventas", con=engine)
    print("\n✅ Datos cargados correctamente en pandas:")
    print(df.head())

except Exception as e:
    print("⚠️ Error al cargar los datos en pandas:", e)
