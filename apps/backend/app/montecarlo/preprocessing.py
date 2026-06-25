import numpy as np
from multiprocessing import Pool, cpu_count

from .core import simulate

def worker(args):
    values, batch_size = args

    local_results = []

    for _ in range(batch_size):
        local_results.append(
            simulate(values)
        )

    return local_results

def run_parallel(values, simulations):

    cores = cpu_count()

    base = simulations // cores
    remainder = simulations % cores

    batches = [
        base + (1 if i < remainder else 0)
        for i in range(cores)
    ]

    worker_args = [
        (values, batch)
        for batch in batches
    ]

    with Pool(cores) as pool:
        chunks = pool.map(
            worker,
            worker_args
        )

    results = np.concatenate(chunks)

    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }