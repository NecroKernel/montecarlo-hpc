# Monte Carlo HPC Simulator ⚡

Un motor de simulación de alto rendimiento (HPC) basado en el método de Monte Carlo para proyectar la dispersión de contaminantes (`PM10`) en Lima (Estación: Campo de Marte). El proyecto compara directamente los tiempos de ejecución entre procesamiento secuencial y paralelo explotando al máximo los núcleos de la CPU en entornos distribuidos de nube (Azure).

## 📂 Estructura del Repositorio

El proyecto está organizado de la siguiente manera basado en una arquitectura orientada a microservicios:

```text
├── apps
│   ├── backend
│   │   ├── app
│   │   │   ├── main.py             # Endpoints de FastAPI y lógica de orquestación
│   │   │   └── montecarlo
│   │   │       ├── core.py         # Motor base: muestreo y resumen estadístico
│   │   │       ├── metrics.py      # Benchmark de tiempos de ejecución
│   │   │       ├── parallel.py     # Paralelización por lotes (multiprocessing.Pool)
│   │   │       ├── preprocessing.py # Carga/filtrado del CSV (cacheado en memoria)
│   │   │       └── sequential.py   # Procesamiento lineal en un único proceso
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
```

## 🏗️ Arquitectura

| Capa | Tecnología | Rol |
|------|-----------|-----|
| Frontend | React 18 + Vite | Dashboard interactivo (selector de fechas y nº de simulaciones) |
| Backend | FastAPI + Uvicorn | API REST que orquesta el pipeline |
| Cómputo | `multiprocessing` + NumPy | Simulación Monte Carlo secuencial vs. paralela por lotes |
| Datos | pandas + CSV (SENAMHI) | Carga y filtrado (cacheado en memoria) |
| Infra | Docker + Azure VM | Contenedores y despliegue en la nube |

> **Nota sobre el modelo:** la simulación usa *remuestreo bootstrap* de los valores
> históricos observados (PM10) para estimar la distribución de concentraciones y la
> probabilidad de superar el umbral de alerta de la OMS (100 µg/m³). No es un modelo
> físico de dispersión atmosférica.

## ▶️ Cómo ejecutar

### Con Docker (recomendado)

```bash
cd infra
docker compose up --build
# Frontend: http://localhost:3000   |   Backend: http://localhost:8000/docs
```

### En local (sin Docker)

**Backend**

```bash
cd apps/backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Apunta al CSV local (fuera de Docker):
export DATA_PATH=../../data/contaminantes_lima.csv   # Windows: set DATA_PATH=...
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend**

```bash
cd apps/frontend
npm install
# Opcional: apuntar a un backend distinto a localhost:8000
echo "VITE_BACKEND_URL=http://localhost:8000" > .env.local
npm run dev   # http://localhost:4173
```

## ⚙️ Variables de entorno

| Variable | Servicio | Por defecto | Descripción |
|----------|----------|-------------|-------------|
| `DATA_PATH` | backend | `/app/data/contaminantes_lima.csv` | Ruta al CSV de datos |
| `ALLOWED_ORIGINS` | backend | `*` | Orígenes CORS permitidos (separados por comas) |
| `VITE_BACKEND_URL` | frontend | `http://localhost:8000` | URL base del backend |

## 📡 API

Ver la especificación completa en [`docs/api_spec.md`](docs/api_spec.md) y la
documentación interactiva en `http://localhost:8000/docs` (Swagger UI).
