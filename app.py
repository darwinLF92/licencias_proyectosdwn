from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_connection():
    try:
        print("Obteniendo conexión a la base de datos...")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        print("Conexión exitosa.")
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", str(e))
        raise

@app.route("/validar-licencia", methods=["GET"])
def validar_licencia():
    nit = request.args.get("nit")
    clave = request.args.get("clave")

    print(f"Parámetros recibidos: nit={nit}, clave={clave}")

    if not nit or not clave:
        return jsonify({"error": "Parámetros 'nit' y 'clave' son requeridos"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT 1 FROM licencias WHERE nit = %s AND clave_fabricacion = %s"
        print("Ejecutando consulta:", query)
        cur.execute(query, (nit, clave))
        result = cur.fetchone()
        cur.close()
        conn.close()

        print("Resultado de la consulta:", result)

        if result:
            return jsonify({"valido": True})
        return jsonify({"valido": False})
    except Exception as e:
        print("Error durante la validación:", str(e))
        return jsonify({"error": str(e)}), 500
