import numpy as np
from multiprocessing import cpu_count

def run_sequential(values, simulations):

    cores = cpu_count()
    base = simulations // cores

    chunk_size = min(250000, base if base > 0 else simulations)

    results = np.empty(simulations, dtype=np.float64)

    i = 0
    while i < simulations:
        current = min(chunk_size, simulations - i)

        matrix = np.random.choice(
            values,
            size=(current, 1000),
            replace=True
        )

        results[i:i+current] = np.mean(matrix, axis=1)
        i += current

    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }