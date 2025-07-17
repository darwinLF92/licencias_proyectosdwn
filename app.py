from flask import Flask, jsonify, request
import psycopg2
from dotenv import load_dotenv
import os
import traceback
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde cualquier origen

# Configuración desde .env
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

@app.route("/")
def home():
    return "¡Servidor Flask corriendo correctamente!"

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
        return jsonify({"error": traceback.format_exc()})

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
        return jsonify({"valido": False, "error": str(e)})

@app.route("/health")
def health():
    return jsonify({
        "db_host": DB_HOST,
        "db_name": DB_NAME,
        "db_port": DB_PORT
    })
