import numpy as np
from multiprocessing import Pool, cpu_count
from .core import simulate

def worker(args):
    values, batch_size = args
    
    # 🚨 OPTIMIZACIÓN 1: Preasignamos un array de NumPy en lugar de usar .append() lento
    local_results = np.empty(batch_size, dtype=np.float64)
    
    for i in range(batch_size):
        local_results[i] = simulate(values)
        
    return local_results # NumPy serializa muchísimo más rápido que las listas nativas

def run_parallel(values, simulations):
    cores = cpu_count() # Detectará tus 2 vCPUs de la VM automáticamente

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

    # 🚨 OPTIMIZACIÓN 2: Concatenar arrays de NumPy es instantáneo en memoria C
    results = np.concatenate(chunks)

    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }