"""Worker de la simulación Monte Carlo.

Se define en un módulo IMPORTABLE (no dentro del notebook) a propósito:
en Windows, `ProcessPoolExecutor`/`multiprocessing` usan el método 'spawn',
que vuelve a importar el código en cada proceso hijo. Una función definida en
el `__main__` de un notebook no se puede re-importar y el Pool falla con
"Can't get attribute ... on module '__main__'". Por eso el avance anterior
había caído en usar ThreadPoolExecutor (que NO paraleliza trabajo CPU-bound por
el GIL). Teniendo el worker aquí, ProcessPool funciona sin problemas.
"""

import numpy as np


def ejecutar_lote_simulacion(args):
    """Ejecuta un lote de simulaciones Monte Carlo.

    Cada iteración genera `n_puntos` valores ~ N(media, std) y guarda su media
    (Teorema del Límite Central). Devuelve el arreglo de medias del lote.

    Recibe un único argumento (una tupla) para ser compatible con `Pool.map`.
    """
    media, std, n_puntos, n_iteraciones_lote = args

    resultados_lote = np.empty(n_iteraciones_lote, dtype=float)
    for i in range(n_iteraciones_lote):
        muestra = np.random.normal(media, std, n_puntos)
        resultados_lote[i] = muestra.mean()

    return resultados_lote
