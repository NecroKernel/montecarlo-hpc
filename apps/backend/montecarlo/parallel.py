import numpy as np

from multiprocessing import Pool
from multiprocessing import cpu_count

def worker(values):
    return np.random.choice(values)

def run_parallel(values, simulations):

    with Pool(cpu_count()) as pool:

        results = pool.map(
            worker,
            [values] * simulations
        )

    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }