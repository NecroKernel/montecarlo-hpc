import numpy as np
from multiprocessing import Pool, cpu_count

def worker(args):
    values, simulations = args

    matrix = np.random.choice(
        values,
        size=(simulations, 1000),
        replace=True
    )

    return np.mean(matrix, axis=1)


def run_parallel(values, simulations):

    cores = cpu_count()

    base = simulations // cores
    remainder = simulations % cores

    batches = [
        base + (1 if i < remainder else 0)
        for i in range(cores)
    ]

    with Pool(cores) as pool:
        chunks = pool.map(worker, [(values, b) for b in batches])

    merged = np.concatenate(chunks)

    return {
        "mean": float(np.mean(merged)),
        "p95": float(np.percentile(merged, 95)),
        "max": float(np.max(merged))
    }