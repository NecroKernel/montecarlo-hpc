import { useState } from "react";

function App() {

  const [result, setResult] = useState(null);

  async function execute() {

    const response = await fetch(
      "http://YOUR_VM_IP:8000/run-comparison",
      {
        method: "POST",
        headers: {
          "Content-Type":"application/json"
        },
        body: JSON.stringify({
          station:"CAMPO_DE_MARTE",
          pollutant:"PM10",
          start_date:"2015-01-01",
          end_date:"2020-12-31",
          simulations:100000
        })
      }
    );

    const data = await response.json();

    setResult(data);
  }

  return (
    <div style={{padding:"2rem"}}>

      <h1>Monte Carlo HPC</h1>

      <button onClick={execute}>
        Ejecutar simulación
      </button>

      {result && (

        <div>

          <h2>Predicción</h2>

          <pre>
            {JSON.stringify(
              result.prediction,
              null,
              2
            )}
          </pre>

          <h2>Performance</h2>

          <pre>
            {JSON.stringify(
              result.performance,
              null,
              2
            )}
          </pre>

        </div>
      )}

    </div>
  );
}

export default App;