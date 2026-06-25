"""Benchmark local: Secuencial vs Paralelo (ProcessPoolExecutor).

Mide y REPORTA los tiempos de ejecución, el speedup y la eficiencia de la
simulación Monte Carlo, barriendo distintos números de procesos. Guarda los
resultados en CSV y JSON para poder graficarlos (ver plot_results.py).

Uso:
    python benchmark_local.py --iteraciones 1000000 --puntos 1000
"""

import argparse
import csv
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

import numpy as np

from montecarlo_worker import ejecutar_lote_simulacion

# Parámetros del fenómeno (calibrados con el dataset de PM10 de Lima).
MEDIA_PM10 = 61.84
STD_PM10 = 46.54

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def _split(total, parts):
    """Reparte `total` iteraciones en `parts` lotes balanceados."""
    base, rem = divmod(total, parts)
    return [base + (1 if i < rem else 0) for i in range(parts)]


def correr_secuencial(media, std, n_puntos, n_iteraciones):
    inicio = time.perf_counter()
    ejecutar_lote_simulacion((media, std, n_puntos, n_iteraciones))
    return time.perf_counter() - inicio


def correr_paralelo(media, std, n_puntos, n_iteraciones, n_procesos):
    tareas = [
        (media, std, n_puntos, n)
        for n in _split(n_iteraciones, n_procesos)
    ]
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=n_procesos) as executor:
        list(executor.map(ejecutar_lote_simulacion, tareas))
    return time.perf_counter() - inicio


def main():
    parser = argparse.ArgumentParser(description="Benchmark Monte Carlo secuencial vs paralelo")
    parser.add_argument("--iteraciones", type=int, default=1_000_000)
    parser.add_argument("--puntos", type=int, default=1000)
    args = parser.parse_args()

    n_iteraciones = args.iteraciones
    n_puntos = args.puntos
    max_cores = cpu_count()
    # Probar potencias de 2 hasta el nº de núcleos disponibles.
    grados = [p for p in (1, 2, 4, 8, 16, 32) if p <= max_cores]

    print(f"=== Benchmark Monte Carlo ===")
    print(f"Iteraciones: {n_iteraciones:,} | Puntos/iteración: {n_puntos} | Núcleos: {max_cores}\n")

    print("Ejecutando versión secuencial (baseline)...")
    t_seq = correr_secuencial(MEDIA_PM10, STD_PM10, n_puntos, n_iteraciones)
    print(f"  Tiempo secuencial: {t_seq:.4f} s\n")

    filas = []
    for p in grados:
        print(f"Ejecutando versión paralela con {p} proceso(s)...")
        t_par = correr_paralelo(MEDIA_PM10, STD_PM10, n_puntos, n_iteraciones, p)
        speedup = t_seq / t_par if t_par > 0 else 0.0
        eficiencia = speedup / p
        filas.append({
            "procesos": p,
            "tiempo_seg": round(t_par, 4),
            "speedup": round(speedup, 3),
            "eficiencia": round(eficiencia, 3),
        })
        print(f"  Tiempo: {t_par:.4f} s | Speedup: {speedup:.2f}x | Eficiencia: {eficiencia:.1%}")

    # --- Reporte final ---
    print("\n=== RESULTADOS ===")
    print(f"{'Procesos':>9} | {'Tiempo (s)':>11} | {'Speedup':>8} | {'Eficiencia':>10}")
    print("-" * 48)
    print(f"{'1 (seq)':>9} | {t_seq:>11.4f} | {'1.00x':>8} | {'100.0%':>10}")
    for f in filas:
        print(f"{f['procesos']:>9} | {f['tiempo_seg']:>11.4f} | {f['speedup']:>7.2f}x | {f['eficiencia']:>9.1%}")

    # --- Persistir resultados ---
    os.makedirs(RESULTS_DIR, exist_ok=True)
    payload = {
        "config": {
            "iteraciones": n_iteraciones,
            "puntos": n_puntos,
            "cpu_cores": max_cores,
            "tiempo_secuencial_seg": round(t_seq, 4),
        },
        "resultados": filas,
    }
    with open(os.path.join(RESULTS_DIR, "benchmark.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(RESULTS_DIR, "benchmark.csv"), "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["procesos", "tiempo_seg", "speedup", "eficiencia"])
        writer.writeheader()
        writer.writerows(filas)

    print(f"\nResultados guardados en: {os.path.abspath(RESULTS_DIR)}")


if __name__ == "__main__":
    main()
