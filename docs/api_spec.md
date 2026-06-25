# Especificación de la API

Base URL (local): `http://localhost:8000`
Documentación interactiva (Swagger): `http://localhost:8000/docs`

---

## `GET /health`

Health check del servicio.

**Respuesta `200 OK`**

```json
{
  "status": "ok",
  "cpu_cores": 8
}
```

---

## `POST /run-comparison`

Ejecuta la simulación Monte Carlo en modo secuencial y paralelo, y devuelve la
predicción estadística junto con las métricas de rendimiento.

### Cuerpo de la petición (`application/json`)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `station` | string | Estación de medición (ej. `CAMPO_DE_MARTE`). |
| `pollutant` | string | Columna del contaminante (ej. `PM10`, `PM2_5`, `NO2`). |
| `start_date` | string (`YYYY-MM-DD`) | Fecha inicial del filtro. |
| `end_date` | string (`YYYY-MM-DD`) | Fecha final del filtro. |
| `simulations` | int | Nº de iteraciones Monte Carlo. Rango: `1` – `10000000`. |

**Ejemplo**

```json
{
  "station": "CAMPO_DE_MARTE",
  "pollutant": "PM10",
  "start_date": "2015-01-01",
  "end_date": "2024-05-31",
  "simulations": 100000
}
```

### Respuesta `200 OK`

```json
{
  "prediction": {
    "expected_mean": 30.73,
    "std_dev": 18.42,
    "min_value": 1.20,
    "max_value": 216.00,
    "p95": 63.31,
    "prob_exceed_100": 2.15,
    "station_analyzed": "CAMPO_DE_MARTE",
    "pollutant_target": "PM10",
    "total_records_filtered": 62313
  },
  "performance": {
    "serial_time_seconds": 0.1563,
    "parallel_time_seconds": 0.0421,
    "speedup_factor": 3.71,
    "efficiency": 0.4638,
    "cpu_cores": 8
  }
}
```

#### Campos de `prediction`

| Campo | Descripción |
|-------|-------------|
| `expected_mean` | Media de las simulaciones (µg/m³). |
| `std_dev` | Desviación estándar. |
| `min_value` / `max_value` | Valor mínimo y máximo simulado. |
| `p95` | Percentil 95. |
| `prob_exceed_100` | Probabilidad (%) de superar 100 µg/m³ (umbral de alerta OMS). |
| `total_records_filtered` | Nº de registros históricos usados como base. |

#### Campos de `performance`

| Campo | Descripción |
|-------|-------------|
| `serial_time_seconds` | Tiempo de la ejecución secuencial. |
| `parallel_time_seconds` | Tiempo de la ejecución paralela. |
| `speedup_factor` | `t_serial / t_parallel`. >1 = el paralelo fue más rápido. |
| `efficiency` | `speedup / cpu_cores`. |
| `cpu_cores` | Núcleos disponibles usados por el pool. |

### Errores

| Código | Causa |
|--------|-------|
| `400` | No hay datos para los filtros, o el contaminante no existe. |
| `422` | Cuerpo inválido (ej. `simulations` fuera de rango). |
| `500` | Error al leer el CSV o durante la ejecución del pipeline. |
