from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd

from modelo_uv import predecir_uv

app = Flask(__name__)
CORS(app)

# 🔹 Conexión a tu MongoDB Atlas
client = MongoClient("mongodb+srv://202311474_db_user:Kishk%40250201@cluster0.zmixzlt.mongodb.net/?appName=Cluster0")
db = client["estacion_uv"]
collection = db["lecturas"]

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.get_json()

    hora_peru = datetime.utcnow() - timedelta(hours=5)
    data["fecha"] = hora_peru.strftime("%Y-%m-%d %H:%M:%S")

    collection.insert_one(data)
    print("Dato guardado:", data)
    return jsonify({"status": "ok"})


@app.route("/datos")
def obtener_datos():
    datos = list(collection.find({}, {"_id": 0}).sort("fecha", -1).limit(20))
    return jsonify(datos)


@app.route("/prediccion")
def prediccion_uv():
    datos = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(datos)

    if df.empty:
        return jsonify({"prediccion": "No hay datos suficientes"})

    pred = predecir_uv(df)
    return jsonify({"prediccion_uv": pred})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
