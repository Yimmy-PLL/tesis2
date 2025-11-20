import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from datetime import datetime

# Variable global para almacenar el modelo entrenado
modelo = None

def entrenar_modelo(df):
    global modelo

    # Asegurar que fecha sea datetime
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    # Crear columna hora
    df["hora"] = df["fecha"].dt.hour

    # Variables de entrada
    X = df[["hora", "temperatura"]]
    y = df["uv"]

    # Definir modelo XGBoost
    modelo = XGBRegressor(
        n_estimators=250,
        learning_rate=0.08,
        max_depth=5,
        objective="reg:squarederror"
    )

    modelo.fit(X, y)
    print("✅ Modelo UV entrenado correctamente.")


def predecir_uv(df):
    global modelo

    # Entrenar solo si no existe un modelo cargado
    if modelo is None:
        entrenar_modelo(df)

    # Datos actuales para la predicción
    hora_actual = datetime.now().hour
    temp_prom = df["temperatura"].tail(5).mean()

    entrada = np.array([[hora_actual, temp_prom]])

    pred = modelo.predict(entrada)[0]

    return float(pred)
