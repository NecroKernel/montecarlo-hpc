import numpy as np

from .core import simulate

def run_sequential(values, simulations):
    # Preasigna memoria igual que el paralelo
    results = np.empty(simulations, dtype=np.float64)
    for i in range(simulations):
        results[i] = simulate(values)
        
    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }