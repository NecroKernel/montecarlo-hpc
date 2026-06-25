# Arquitectura

## Visión general

El sistema sigue una arquitectura de microservicios desacoplada en dos capas
(frontend y backend) más una capa de datos, contenerizada con Docker y
desplegable en una VM de Azure.

```
┌──────────────────┐        POST /run-comparison        ┌──────────────────────┐
│  Frontend (Vite) │ ──────────── JSON ───────────────► │   Backend (FastAPI)  │
│   React 18       │ ◄──────────── JSON ─────────────── │      Uvicorn          │
│   :4173 / :3000  │                                     │       :8000           │
└──────────────────┘                                     └───────────┬──────────┘
                                                                      │
                                          ┌───────────────────────────┼───────────────────────────┐
                                          ▼                           ▼                            ▼
                                 preprocessing.py            sequential.py                 parallel.py
                                 (pandas, CSV cacheado)   (bucle, 1 proceso)      (multiprocessing.Pool, por lotes)
                                          │                           │                            │
                                          └──────────────► core.py (muestreo + summarize) ◄────────┘
```

## Componentes del backend

| Módulo | Responsabilidad |
|--------|-----------------|
| `app/main.py` | Define la API FastAPI, valida la petición y orquesta el pipeline. |
| `montecarlo/preprocessing.py` | Carga el CSV **una sola vez** (`lru_cache`) y lo filtra por estación, contaminante y rango de fechas. |
| `montecarlo/core.py` | Funciones base: `simulate` (1 muestra), `simulate_batch` (N muestras vectorizadas) y `summarize` (métricas estadísticas). |
| `montecarlo/sequential.py` | Ejecuta las simulaciones en un único proceso (baseline). |
| `montecarlo/parallel.py` | Reparte las simulaciones en lotes entre `cpu_count()` procesos. |
| `montecarlo/metrics.py` | Mide el tiempo de ejecución (`time.perf_counter`). |

## Flujo de una petición

1. El frontend envía `station`, `pollutant`, `start_date`, `end_date` y `simulations`.
2. `preprocessing` devuelve el arreglo de valores históricos filtrados.
3. Se ejecuta y cronometra la versión **secuencial** y la **paralela** sobre los mismos datos.
4. Se calcula **speedup** = t_serial / t_parallel y **eficiencia** = speedup / nº cores.
5. Se devuelve un JSON con la predicción estadística y las métricas de rendimiento.

## Decisión de diseño: paralelización por lotes

La versión inicial enviaba el arreglo completo de datos a un worker **por cada
simulación** (`pool.map(worker, [values] * simulations)`). El costo de serializar
(pickle) y transferir los datos entre procesos (IPC) superaba con creces el costo
de cada muestra individual, haciendo que la versión "paralela" fuera órdenes de
magnitud **más lenta** que la secuencial (speedup ≈ 0.04).

La versión actual reparte las `N` simulaciones en `cpu_count()` lotes: cada worker
recibe el arreglo una sola vez y genera su lote de forma vectorizada con NumPy.
Esto reduce el overhead de IPC de O(N) a O(nº de procesos).

## Modelo estadístico

Se aplica **remuestreo bootstrap**: cada simulación toma una muestra aleatoria de
los valores históricos observados. Con muchas iteraciones se reconstruye la
distribución empírica, de la que se derivan media, desviación, percentil 95 y la
probabilidad de superar el umbral de alerta de la OMS (100 µg/m³ para PM10).

## Escalabilidad y despliegue

- **Contenedores:** `Dockerfile` por servicio + `docker-compose.yml`.
- **CI:** GitHub Actions construye la imagen del backend en cada push a `main`.
- **Nube:** despliegue en VM de Azure; el CSV se monta como volumen (`/app/data`).
