import numpy as np

def simulate(values):
    """
    Una simulación Monte Carlo.
    Cada simulación toma 1000 muestras aleatorias
    y devuelve su media.
    """

    samples = np.random.choice(
        values,
        size=1000,
        replace=True
    )

    return np.mean(samples)