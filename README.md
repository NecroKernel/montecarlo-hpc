# Monte Carlo HPC Simulator: Quality Air Data Pipeline & Analytics

Este proyecto es una plataforma de analítica avanzada y computación de alto rendimiento (HPC) que implementa simulaciones estocásticas de Monte Carlo para proyectar el comportamiento y mitigar riesgos asociados a la contaminación del aire ($PM_{10}$) en Lima Metropolitana, utilizando datos históricos oficiales del SENAMHI.

La arquitectura está diseñada bajo principios de desacoplamiento de componentes, procesamiento en paralelo vectorizado para exprimir el hardware en la nube y despliegue automatizado mediante contenedores Docker sobre infraestructura Microsoft Azure.

---

## 📁 Estructura Completa del Proyecto

El repositorio está organizado siguiendo patrones de diseño modulares para separar de forma estricta la lógica del cliente web, las operaciones del servidor de cómputo y los archivos de configuración de infraestructura:

```text
montecarlo-hpc/
├── backend/                  # Servidor de Cómputo (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Definición de Endpoints de FastAPI (/run-comparison)
│   │   ├── core.py          # Lógica base de la simulación matemática
│   │   └── montecarlo/
│   │       ├── __init__.py
│   │       ├── preprocessing.py # Ingesta y filtrado temporal de series históricas
│   │       ├── sequential.py    # Algoritmo secuencial con Dynamic Mini-Batching
│   │       ├── parallel.py      # Algoritmo paralelo vectorizado distribuido
│   │       └── metrics.py       # Wrapper de benchmark de tiempo de ejecución
│   ├── data/
│   │   └── contaminantes_lima.csv  # Series temporales históricas de SENAMHI
│   ├── Dockerfile            # Configuración de compilación para el Backend
│   └── requirements.txt      # Dependencias core de Python (FastAPI, NumPy, Pandas)
├── frontend/                 # Aplicación Web (React.js)
│   ├── src/
│   │   ├── components/      # Componentes UI (Formularios, Tarjetas de Métricas)
│   │   ├── App.jsx          # Componente principal y gestión de estado
│   │   └── main.jsx
│   ├── package.json          # Dependencias y scripts de Node.js
│   └── Dockerfile            # Configuración de compilación para el Frontend
└── infra/                    # Capa de Orquestación y Despliegue
    ├── .env                  # Variables de entorno (Puertos, IPs)
    └── docker-compose.yml    # Manifiesto multiservicio de producción


