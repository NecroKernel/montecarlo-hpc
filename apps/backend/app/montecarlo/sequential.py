import numpy as np

from .core import simulate

def run_sequential(values, simulations):

    results = []

    for _ in range(simulations):
        results.append(simulate(values))

    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }