from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

@app.route("/validar-licencia", methods=["GET"])
def validar_licencia():
    nit = request.args.get("nit")
    clave = request.args.get("clave")

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM licencias WHERE nit = %s AND clave_fabricacion = %s", (nit, clave))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify({"valido": True})
        return jsonify({"valido": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

