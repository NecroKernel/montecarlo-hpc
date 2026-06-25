import numpy as np

# Límite de alerta de la OMS para PM10 (µg/m³), usado en el análisis de riesgo.
ALERT_THRESHOLD = 100.0


def simulate(values):
    """Una sola muestra Monte Carlo (remuestreo bootstrap de los datos históricos)."""
    return np.random.choice(values)


def simulate_batch(values, n):
    """Genera `n` muestras Monte Carlo de forma vectorizada.

    Mucho más eficiente que llamar a `simulate` en un bucle: NumPy realiza
    el muestreo en C sobre todo el lote de una sola vez.
    """
    return np.random.choice(values, size=n)


def summarize(results, threshold=ALERT_THRESHOLD):
    """Resume un arreglo de resultados Monte Carlo en métricas estadísticas.

    Centraliza el cálculo para que las versiones secuencial y paralela
    devuelvan exactamente la misma estructura (comparación justa).
    """
    results = np.asarray(results, dtype=float)
    return {
        "mean": float(np.mean(results)),
        "std": float(np.std(results)),
        "min": float(np.min(results)),
        "max": float(np.max(results)),
        "p95": float(np.percentile(results, 95)),
        # Probabilidad (%) de superar el umbral de alerta de la OMS.
        "prob_exceed": float(np.mean(results > threshold) * 100.0),
    }
