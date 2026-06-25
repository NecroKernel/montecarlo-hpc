import os
from functools import lru_cache

import pandas as pd

# Permite sobrescribir la ruta del CSV vía variable de entorno (para correr
# fuera de Docker). Por defecto usa la ruta del contenedor.
DATA_PATH = os.environ.get("DATA_PATH", "/app/data/contaminantes_lima.csv")


@lru_cache(maxsize=1)
def _load_df():
    """Carga y parsea el CSV UNA sola vez (se cachea en memoria).

    El dataset tiene ~578k filas; releerlo y reparsear las fechas en cada
    request era el mayor costo de latencia. Con la caché, el primer request
    paga el costo y los siguientes reutilizan el DataFrame ya procesado.
    """
    df = pd.read_csv(DATA_PATH)
    df["FECHA"] = pd.to_datetime(
        df["FECHA"].astype(str),
        format="%Y%m%d"
    )
    return df


def get_filtered_values(
    station,
    pollutant,
    start_date,
    end_date
):
    df = _load_df()

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered = df[
        (df["ESTACION"] == station)
        & (df["FECHA"] >= start_date)
        & (df["FECHA"] <= end_date)
    ]

    values = (
        filtered[pollutant]
        .dropna()
        .astype(float)
        .values
    )

    if len(values) == 0:
        raise ValueError("No hay datos para los filtros seleccionados")

    return values
