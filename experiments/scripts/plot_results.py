"""Grafica los resultados del benchmark (speedup y eficiencia vs nº de procesos).

Lee experiments/results/benchmark.json (generado por benchmark_local.py) y
guarda dos PNG listos para la presentación.

Uso:
    python plot_results.py
"""

import json
import os

import matplotlib
matplotlib.use("Agg")  # backend no interactivo: solo guardamos PNGs
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def main():
    with open(os.path.join(RESULTS_DIR, "benchmark.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    res = data["resultados"]
    procesos = [r["procesos"] for r in res]
    speedup = [r["speedup"] for r in res]
    eficiencia = [r["eficiencia"] * 100 for r in res]
    ideal = procesos  # speedup ideal (lineal) = nº de procesos

    # --- Gráfico 1: Speedup ---
    plt.figure(figsize=(8, 5))
    plt.plot(procesos, speedup, "o-", color="#0284c7", linewidth=2, label="Speedup real")
    plt.plot(procesos, ideal, "--", color="#94a3b8", label="Speedup ideal (lineal)")
    plt.axhline(1.0, color="#ef4444", linestyle=":", label="Baseline secuencial")
    plt.title("Speedup vs Número de Procesos (ProcessPoolExecutor)")
    plt.xlabel("Número de procesos")
    plt.ylabel("Speedup (x)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "speedup.png"), dpi=150)

    # --- Gráfico 2: Eficiencia ---
    plt.figure(figsize=(8, 5))
    plt.plot(procesos, eficiencia, "s-", color="#22c55e", linewidth=2)
    plt.axhline(100, color="#94a3b8", linestyle="--", label="Eficiencia ideal (100%)")
    plt.title("Eficiencia vs Número de Procesos")
    plt.xlabel("Número de procesos")
    plt.ylabel("Eficiencia (%)")
    plt.ylim(0, 110)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "eficiencia.png"), dpi=150)

    print(f"Gráficos guardados en: {os.path.abspath(RESULTS_DIR)}")
    print("  - speedup.png")
    print("  - eficiencia.png")


if __name__ == "__main__":
    main()
