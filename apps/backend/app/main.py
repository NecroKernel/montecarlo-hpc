from fastapi import FastAPI
from pydantic import BaseModel

from montecarlo.preprocessing import get_filtered_values
from montecarlo.sequential import run_sequential
from montecarlo.parallel import run_parallel
from montecarlo.metrics import benchmark

app = FastAPI(title="Monte Carlo HPC")

class SimulationRequest(BaseModel):
    station: str
    pollutant: str
    start_date: str
    end_date: str
    simulations: int

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/run-comparison")
def run_comparison(req: SimulationRequest):

    values = get_filtered_values(
        station=req.station,
        pollutant=req.pollutant,
        start_date=req.start_date,
        end_date=req.end_date
    )

    seq_time, seq_result = benchmark(
        run_sequential,
        values,
        req.simulations
    )

    par_time, par_result = benchmark(
        run_parallel,
        values,
        req.simulations
    )

    return {
        "prediction": {
            "sequential": seq_result,
            "parallel": par_result
        },
        "performance": {
            "sequential_time": round(seq_time, 4),
            "parallel_time": round(par_time, 4),
            "speedup": round(seq_time / par_time, 2)
        }
    }