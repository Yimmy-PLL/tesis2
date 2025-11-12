from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 🔹 Conecta con tu base de datos MongoDB Atlas
client = MongoClient("mongodb+srv://202311474_db_user:Kishk%40250201@cluster0.zmixzlt.mongodb.net/?appName=Cluster0")  # ← Pega aquí tu cadena de conexión
db = client["estacion_uv"]
collection = db["lecturas"]

@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.get_json()
    data["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    collection.insert_one(data)
    print("Dato guardado:", data)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
