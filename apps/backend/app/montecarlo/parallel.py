import numpy as np
from multiprocessing import Pool, cpu_count

def batch_worker(args):
    """
    Cada worker recibe el array completo UNA SOLA VEZ 
    y ejecuta su propio lote de simulaciones internamente.
    """
    values, batch_size = args
    # Cada worker genera todo su lote internamente de golpe
    return np.random.choice(values, size=batch_size).tolist()

def run_parallel(values, simulations):
    num_cores = cpu_count()
    
    # Dividimos equitativamente las simulaciones entre los cores disponibles
    base_batch = simulations // num_cores
    remainder = simulations % num_cores
    
    # Crear los tamaños de lote para cada proceso
    batches = [base_batch + (1 if i < remainder else 0) for i in range(num_cores)]
    
    # Empaquetamos los argumentos para cada worker (solo pasamos el array num_cores veces)
    worker_args = [(values, batch_size) for batch_size in batches if batch_size > 0]
    
    with Pool(num_cores) as pool:
        # pool.map ahora solo maneja una lista del tamaño de tus cores (ej. 4 o 8 elementos)
        chunk_results = pool.map(batch_worker, worker_args)
    
    # Aplanamos la lista de listas en un solo array plano de resultados
    results = np.concatenate(chunk_results)
    
    return {
        "mean": float(np.mean(results)),
        "p95": float(np.percentile(results, 95)),
        "max": float(np.max(results))
    }