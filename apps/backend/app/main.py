import os
from multiprocessing import cpu_count

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date

from app.montecarlo.preprocessing import get_filtered_values
from app.montecarlo.sequential import run_sequential
from app.montecarlo.parallel import run_parallel
from app.montecarlo.metrics import benchmark

app = FastAPI(title="Monte Carlo HPC Engine")

# Orígenes permitidos para CORS. Configurable vía ALLOWED_ORIGINS (lista
# separada por comas). Por defecto "*" para desarrollo.
_origins = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    # allow_credentials no puede ser True junto con "*" (lo prohíbe la spec CORS).
    allow_credentials=_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    station: str
    pollutant: str
    start_date: date
    end_date: date
    # Validación: al menos 1 simulación, tope razonable para proteger el servidor.
    simulations: int = Field(gt=0, le=10_000_000)


@app.get("/health")
def health():
    """Endpoint de salud para health checks / monitoreo."""
    return {"status": "ok", "cpu_cores": cpu_count()}


@app.post("/run-comparison")
def run_comparison(request: SimulationRequest):
    try:
        start_str = request.start_date.strftime("%Y-%m-%d")
        end_str = request.end_date.strftime("%Y-%m-%d")

        values = get_filtered_values(
            station=request.station,
            pollutant=request.pollutant,
            start_date=start_str,
            end_date=end_str
        )

    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"El contaminante '{request.pollutant}' no existe en el dataset"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el CSV: {str(e)}")

    try:
        # Benchmark de ambas estrategias sobre los mismos datos.
        serial_time, sequential_results = benchmark(
            run_sequential,
            values,
            request.simulations
        )

        parallel_time, parallel_results = benchmark(
            run_parallel,
            values,
            request.simulations
        )

        # Factor de aceleración. >1 significa que el paralelo fue más rápido.
        speedup = serial_time / parallel_time if parallel_time > 0 else 1.0
        cores = cpu_count()

        return {
            "prediction": {
                "expected_mean": round(parallel_results["mean"], 2),
                "std_dev": round(parallel_results["std"], 2),
                "min_value": round(parallel_results["min"], 2),
                "max_value": round(parallel_results["max"], 2),
                "p95": round(parallel_results["p95"], 2),
                # Probabilidad (%) de superar el umbral de alerta OMS (100 µg/m³).
                "prob_exceed_100": round(parallel_results["prob_exceed"], 2),
                "station_analyzed": request.station,
                "pollutant_target": request.pollutant,
                "total_records_filtered": len(values)
            },
            "performance": {
                "serial_time_seconds": round(serial_time, 4),
                "parallel_time_seconds": round(parallel_time, 4),
                "speedup_factor": round(speedup, 2),
                # Eficiencia = Speedup / nº de procesadores (métrica HPC).
                "efficiency": round(speedup / cores, 4) if cores else 0.0,
                "cpu_cores": cores
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la ejecución del pipeline HPC: {str(e)}")
