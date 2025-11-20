from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import os

from modelo_uv import predecir_uv

app = Flask(__name__, static_url_path='', static_folder='.')

CORS(app)

client = MongoClient("mongodb+srv://202311474_db_user:Kishk%40250201@cluster0.zmixzlt.mongodb.net/?appName=Cluster0")
db = client["estacion_uv"]
collection = db["lecturas"]

# Página principal
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Archivos estáticos (CSS, JS)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# Recibir datos ESP32
@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.get_json()
    hora_peru = datetime.utcnow() - timedelta(hours=5)
    data["fecha"] = hora_peru.strftime("%Y-%m-%d %H:%M:%S")
    collection.insert_one(data)
    return jsonify({"status": "ok"})

# Últimos 20 datos
@app.route("/datos")
def obtener_datos():
    datos = list(collection.find({}, {"_id": 0}).sort("fecha", -1).limit(20))
    return jsonify(datos)

# Predicción UV
@app.route("/prediccion")
def prediccion_uv():
    datos = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(datos)

    if df.empty or len(df) < 10:
        return jsonify({"prediccion_uv": "No hay datos suficientes para predecir"})

    pred = predecir_uv(df)
    return jsonify({"prediccion_uv": float(pred)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
