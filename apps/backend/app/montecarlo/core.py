import numpy as np

def run_sequential(values, simulations):
    # Genera todas las muestras de golpe: una matriz de (simulations, 1000)
    matrix = np.random.choice(values, size=(simulations, 1000), replace=True)
    
    # Calcula la media a lo largo del eje de cada simulación (axis=1)
    results = np.mean(matrix, axis=1)
    
    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }