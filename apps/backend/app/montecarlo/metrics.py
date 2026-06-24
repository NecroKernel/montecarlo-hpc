import time

def benchmark(func, values, simulations):

    start = time.perf_counter()

    result = func(
        values,
        simulations
    )

    end = time.perf_counter()

    return end - start, result