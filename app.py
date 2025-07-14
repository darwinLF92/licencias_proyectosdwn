from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO)


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

    logging.info(f"Solicitud recibida para NIT: {nit}, Clave: {clave}")
    
    try:
        print("Conectando a base de datos...")
        conn = get_connection()
        logging.info("Conexión a la base de datos establecida correctamente.")
        
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM licencias WHERE nit = %s AND clave_fabricacion = %s", (nit, clave))
        result = cur.fetchone()
        cur.close()
        conn.close()

        logging.info(f"Resultado de validación: {result}")
        
        if result:
            return jsonify({"valido": True})
        return jsonify({"valido": False})
        
    except Exception as e:
        logging.error(f"Error al validar licencia: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
