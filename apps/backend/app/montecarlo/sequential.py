import numpy as np

from .core import simulate, summarize


def run_sequential(values, simulations):
    """Baseline secuencial: una muestra a la vez en un único proceso.

    Representa el enfoque "ingenuo". Sirve como punto de comparación contra
    la versión paralela para calcular el speedup.
    """
    results = np.empty(simulations, dtype=float)

    for i in range(simulations):
        results[i] = simulate(values)

    return summarize(results)
