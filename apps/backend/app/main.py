import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date

# Imports basados exactamente en tu estructura de archivos vista en VS Code
from app.montecarlo.preprocessing import get_filtered_values
from app.montecarlo.sequential import run_sequential
from app.montecarlo.parallel import run_parallel
from app.montecarlo.metrics import benchmark

app = FastAPI(title="Monte Carlo HPC Engine")

# Habilitar CORS para que tu frontend en el puerto 3000 no se bloquee
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estructura del payload que viene desde tu formulario de React
class SimulationRequest(BaseModel):
    station: str
    pollutant: str
    start_date: date
    end_date: date
    simulations: int

@app.post("/run-comparison")
def run_comparison(request: SimulationRequest):
    try:
        # 1. Obtener los valores filtrados del CSV usando función de preprocessing.py
        # Convertimos las fechas a string ya que tu pandas filter hace .astype(str) o comparación limpia
        start_str = request.start_date.strftime("%Y-%m-%d")
        end_str = request.end_date.strftime("%Y-%m-%d")
        
        values = get_filtered_values(
            station=request.station,
            pollutant=request.pollutant,
            start_date=start_str,
            end_date=end_str
        )
        
    except ValueError as val_err:
        # Captura el raise ValueError("No hay datos para los filtros seleccionados")
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el CSV: {str(e)}")

    try:
        # 2. Correr y tomar tiempos usando función benchmark(func, values, simulations) de metrics.py
        # Simulación Secuencial
        serial_time, sequential_results = benchmark(
            run_sequential, 
            values, 
            request.simulations
        )
        
        # Simulación Paralela 
        parallel_time, parallel_results = benchmark(
            run_parallel, 
            values, 
            request.simulations
        )
        
        # 3. Calcular el factor de aceleración (Speedup)
        speedup = serial_time / parallel_time if parallel_time > 0 else 1.0

        # Retornamos la estructura exacta de JSON que mapea con los campos de tu App.jsx
        return {
            "prediction": {
                "expected_mean": round(float(parallel_results.get("mean", 0)), 2),
                "max_value": round(float(parallel_results.get("max", 0)), 2),      
                "p95_value": round(float(parallel_results.get("p95", 0)), 2),      
                "station_analyzed": request.station,
                "pollutant_target": request.pollutant,
                "total_records_filtered": len(values)
            },
            "performance": {
                "serial_time_seconds": round(serial_time, 4),
                "parallel_time_seconds": round(parallel_time, 4),
                "speedup_factor": round(speedup, 2)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la ejecución del pipeline HPC: {str(e)}")