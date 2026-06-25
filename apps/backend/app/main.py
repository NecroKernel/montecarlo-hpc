from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date

from app.montecarlo.preprocessing import get_filtered_values
from app.montecarlo.sequential import run_sequential
from app.montecarlo.parallel import run_parallel
from app.montecarlo.metrics import benchmark

app = FastAPI(title="Monte Carlo HPC Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    station: str
    pollutant: str
    start_date: date
    end_date: date
    simulations: int


@app.post("/run-comparison")
def run_comparison(request: SimulationRequest):

    try:
        values = get_filtered_values(
            station=request.station,
            pollutant=request.pollutant,
            start_date=request.start_date,
            end_date=request.end_date
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing error: {str(e)}")

    try:
        serial_time, _ = benchmark(run_sequential, values, request.simulations)
        parallel_time, parallel_results = benchmark(run_parallel, values, request.simulations)

        speedup = serial_time / parallel_time if parallel_time > 0 else 1.0

        return {
            "prediction": {
                "expected_mean": float(parallel_results["mean"]),
                "p95_value": float(parallel_results["p95"]),
                "max_value": float(parallel_results["max"]),
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
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")