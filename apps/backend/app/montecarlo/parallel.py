import numpy as np

from multiprocessing import Pool, cpu_count

from .core import simulate_batch, summarize


def worker(task):
    """Cada worker genera un LOTE completo de simulaciones, no una sola.

    El array `values` se serializa (pickle) una vez por proceso —no una vez
    por simulación— y el muestreo se hace vectorizado. Esto elimina el cuello
    de botella de comunicación (IPC) que hacía que la versión anterior fuera
    más lenta que la secuencial.
    """
    values, n = task
    return simulate_batch(values, n)


def _split(total, parts):
    """Reparte `total` simulaciones en `parts` lotes lo más balanceados posible."""
    base, rem = divmod(total, parts)
    sizes = [base + (1 if i < rem else 0) for i in range(parts)]
    return [s for s in sizes if s > 0]


def run_parallel(values, simulations):
    n_workers = cpu_count()
    chunks = _split(simulations, n_workers)

    with Pool(len(chunks)) as pool:
        parts = pool.map(
            worker,
            [(values, n) for n in chunks]
        )

    results = np.concatenate(parts)

    return summarize(results)
