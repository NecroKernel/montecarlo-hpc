import numpy as np
from multiprocessing import Pool, cpu_count

def worker(args):
    values, batch_size = args
    # Cada core genera su matriz local de un solo golpe en C
    matrix = np.random.choice(values, size=(batch_size, 1000), replace=True)
    return np.mean(matrix, axis=1)

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
        chunks = pool.map(worker, worker_args)

    results = np.concatenate(chunks)

    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }