import pandas as pd

DATA_PATH = "/app/data/contaminantes_lima.csv"

def get_filtered_values(
    station,
    pollutant,
    start_date,
    end_date
):

    df = pd.read_csv(DATA_PATH)

    df["FECHA"] = pd.to_datetime(
        df["FECHA"].astype(str),
        format="%Y%m%d"
    )

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