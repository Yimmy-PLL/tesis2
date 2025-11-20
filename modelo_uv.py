import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from datetime import datetime

modelo = None

def entrenar_modelo(df):
    global modelo

    df["hora"] = pd.to_datetime(df["fecha"]).dt.hour
    X = df[["hora", "temperatura"]]
    y = df["uv"]

    modelo = XGBRegressor(
        n_estimators=250,
        learning_rate=0.08,
        max_depth=5
    )

    modelo.fit(X, y)
    print("Modelo UV entrenado correctamente.")


def predecir_uv(df):
    global modelo

    if modelo is None:
        entrenar_modelo(df)

    hora_actual = datetime.now().hour
    temp_prom = df["temperatura"].tail(5).mean()

    entrada = np.array([[hora_actual, temp_prom]])
    pred = modelo.predict(entrada)[0]

    return float(pred)
