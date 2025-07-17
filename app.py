from flask import Flask, jsonify, request
import psycopg2
from dotenv import load_dotenv
import os
import traceback
from flask_cors import CORS

# Cargar variables de entorno desde .env
load_dotenv()

# Inicializar app Flask
app = Flask(__name__)
CORS(app)  # Permite CORS para todos los orígenes

print("✅ Flask app cargada correctamente")

# Configuración de base de datos desde variables de entorno
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

print("📡 Conexión DB:")
print("  HOST:", DB_HOST)
print("  NAME:", DB_NAME)
print("  USER:", DB_USER)
print("  PORT:", DB_PORT)

# Ruta principal
@app.route("/")
def home():
    return "¡Servidor Flask corriendo correctamente!"

# Ruta para verificar estado (útil para debugging en Railway)
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "db_host": DB_HOST,
        "db_name": DB_NAME,
        "db_port": DB_PORT
    })

# Ruta para obtener todas las licencias
@app.route("/licencias")
def obtener_licencias():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_empresa, clave_fabricacion FROM licencias")
        filas = cursor.fetchall()

        columnas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in filas]

        cursor.close()
        conn.close()

        return jsonify(resultados)

    except Exception as e:
        error_msg = traceback.format_exc()
        print("❌ Error al obtener licencias:\n", error_msg)
        return jsonify({"error": error_msg})

# Ruta para validar licencia
@app.route("/validar_licencia", methods=["POST"])
def validar_licencia():
    try:
        data = request.get_json()
        nit = data.get("nit")
        clave = data.get("clave_fabricacion")

        if not nit or not clave:
            return jsonify({"valido": False, "error": "Faltan datos"}), 400

        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM licencias WHERE nit = %s AND clave_fabricacion = %s",
            (nit, clave)
        )
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:
            return jsonify({"valido": True})
        else:
            return jsonify({"valido": False, "error": "Datos incorrectos"})

    except Exception as e:
        error_msg = traceback.format_exc()
        print("❌ Error al validar licencia:\n", error_msg)
        return jsonify({"valido": False, "error": str(e)})

# 👇 No incluimos app.run() aquí porque Railway usa Gunicorn
# app.py se ejecuta con gunicorn: `gunicorn -b 0.0.0.0:8080 app:app`
