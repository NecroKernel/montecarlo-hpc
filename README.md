# Monte Carlo HPC Simulator ⚡

Un motor de simulación de alto rendimiento (HPC) basado en el método de Monte Carlo para proyectar la dispersión de contaminantes (`PM10`) en Lima (Estación: Campo de Marte). El proyecto compara directamente los tiempos de ejecución entre procesamiento secuencial y paralelo explotando al máximo los núcleos de la CPU en entornos distribuidos de nube (Azure).

## 📂 Estructura del Repositorio

El proyecto está organizado de la siguiente manera basado en una arquitectura orientada a microservicios:

```text
├── apps
│   ├── backend
│   │   ├── app
│   │   │   └── api
│   │   │       └── main.py          # Endpoints de FastAPI y lógica de orquestación
│   │   ├── montecarlo
│   │   │   ├── core.py             # Motor matemático base del simulador
│   │   │   ├── metrics.py          # Cálculo de velocidad de procesamiento y speedup
│   │   │   ├── parallel.py         # Orquestación con multiprocessing (Pool mapping)
│   │   │   ├── preprocessing.py    # Transformaciones y pipelines de datos de entrada
│   │   │   └── sequential.py       # Procesamiento lineal en un único hilo
│   │   ├── Dockerfile
│   │   └── requirements.txt        # Dependencias backend (FastAPI, NumPy, Uvicorn)
│   └── frontend
│       ├── src
│       │   ├── App.jsx             # Panel Dashboard interactivo (Dark Theme) con selector de fechas
│       │   └── main.jsx            # Punto de entrada de la aplicación React 18
│       ├── Dockerfile
│       ├── package.json            # Configuración de dependencias (Vite 5, React)
│       └── vite.config.js          # Configuración del servidor de desarrollo/preview y plugins
├── data
│   └── contaminantes_lima.csv      # Dataset histórico de entrada para calibrar la simulación
├── experiments                     # Cuadernos de Jupyter con análisis estadísticos previos
│   ├── montecarlo_secuencial.ipynb
│   └── montecarlo_secuencial_vs_paralelo.ipynb
└── infra
    ├── docker-compose.yml          # Orquestación global de contenedores en red interna
    └── nginx                       # Configuración opcional para proxy inverso
