import { useState } from "react";

function App() {
  // 1. Dynamic Form States
  const [startDate, setStartDate] = useState("2015-01-01");
  const [endDate, setEndDate] = useState("2024-05-31");
  const [simulations, setSimulations] = useState(100000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Target your working Azure Public IP
  const BACKEND_URL = "http://20.114.170.13:8000/run-comparison";

  async function execute(e) {
    e.preventDefault(); // Prevent page refresh on form submit
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(BACKEND_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          station: "CAMPO_DE_MARTE",
          pollutant: "PM10",
          start_date: startDate,
          end_date: endDate,
          simulations: parseInt(simulations),
        }),
      });

      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to connect to the backend execution layer.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#0f172a", // Deep slate background
      color: "#f8fafc",
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      padding: "2rem 1rem",
      boxSizing: "border-box"
    }}>
      <div style={{ maxWidth: "1000px", margin: "0 auto" }}>
        
        {/* Header */}
        <header style={{ borderBottom: "1px solid #334155", paddingBottom: "1.5rem", marginBottom: "2rem" }}>
          <h1 style={{ fontSize: "2.25rem", fontWeight: "700", color: "#38bdf8", margin: 0 }}>
            Monte Carlo HPC Simulator
          </h1>
          <p style={{ color: "#94a3b8", marginTop: "0.5rem", fontSize: "0.95rem" }}>
            High-Performance Compute Data Analysis Pipeline
          </p>
        </header>

        {/* Input Configuration Panel */}
        <div style={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "1.5rem", marginBottom: "2rem" }}>
          <h3 style={{ margin: "0 0 1.25rem 0", color: "#f1f5f9", fontSize: "1.1rem" }}>Simulation Parameters</h3>
          
          <form onSubmit={execute}>
            <div style={{ display: "flex", gap: "1.5rem", flexWrap: "wrap", marginBottom: "1.5rem" }}>
              <div style={{ flex: "1 1 200px" }}>
                <label style={{ display: "block", marginBottom: "0.5rem", fontSize: "0.85rem", color: "#94a3b8", fontWeight: "600" }}>START DATE</label>
                <input 
                  type="date" 
                  required 
                  style={{ width: "100%", padding: "0.6rem", borderRadius: "6px", border: "1px solid #475569", backgroundColor: "#0f172a", color: "#fff", boxSizing: "border-box" }} 
                  value={startDate} 
                  onChange={e => setStartDate(e.target.value)} 
                />
              </div>
              <div style={{ flex: "1 1 200px" }}>
                <label style={{ display: "block", marginBottom: "0.5rem", fontSize: "0.85rem", color: "#94a3b8", fontWeight: "600" }}>END DATE</label>
                <input 
                  type="date" 
                  required 
                  style={{ width: "100%", padding: "0.6rem", borderRadius: "6px", border: "1px solid #475569", backgroundColor: "#0f172a", color: "#fff", boxSizing: "border-box" }} 
                  value={endDate} 
                  onChange={e => setEndDate(e.target.value)} 
                />
              </div>
              <div style={{ flex: "1 1 200px" }}>
                <label style={{ display: "block", marginBottom: "0.5rem", fontSize: "0.85rem", color: "#94a3b8", fontWeight: "600" }}>SIMULATION RUNS</label>
                <input 
                  type="number" 
                  required
                  style={{ width: "100%", padding: "0.6rem", borderRadius: "6px", border: "1px solid #475569", backgroundColor: "#0f172a", color: "#fff", boxSizing: "border-box" }} 
                  value={simulations} 
                  onChange={e => setSimulations(e.target.value)} 
                  min="1000" 
                  max="1000000" 
                />
              </div>
            </div>
            
            <button 
              type="submit" 
              disabled={loading} 
              style={{ 
                backgroundColor: loading ? "#0284c7" : "#0284c7", 
                opacity: loading ? 0.6 : 1,
                color: "white", 
                padding: "0.75rem 1.5rem", 
                border: "none", 
                borderRadius: "6px", 
                fontWeight: "600", 
                cursor: loading ? "not-allowed" : "pointer", 
                width: "100%", 
                fontSize: "1rem",
                transition: "background-color 0.2s"
              }}
            >
              {loading ? "Executing Jobs Across Cloud Kernels..." : "Run HPC Computation Pipeline ⚡"}
            </button>
          </form>
        </div>

        {error && (
          <div style={{ backgroundColor: "#7f1d1d", border: "1px solid #f87171", color: "#fef2f2", padding: "1rem", borderRadius: "8px", marginBottom: "2rem" }}>
            ⚠️ Error: {error}
          </div>
        )}

        {/* Dashboard Analytics View */}
        {result && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "2rem" }}>
            
            {/* Performance Matrix Row */}
            <div>
              <h2 style={{ fontSize: "1.3rem", color: "#f1f5f9", marginBottom: "1rem", fontWeight: "600" }}>Execution Benchmark Performance</h2>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "1.25rem" }}>
                
                <div style={{ backgroundColor: "#1e293b", border: "1px solid #334155", padding: "1.25rem", borderRadius: "8px" }}>
                  <span style={{ fontSize: "0.75rem", color: "#94a3b8", fontWeight: "700", letterSpacing: "0.05em" }}>SERIAL RUNTIME</span>
                  <div style={{ fontSize: "2rem", fontWeight: "700", color: "#ef4444", margin: "0.5rem 0" }}>
                    {result.performance?.serial_time_seconds || result.performance?.serial || "N/A"}s
                  </div>
                  <small style={{ color: "#64748b" }}>Isolated CPU main thread execution</small>
                </div>

                <div style={{ backgroundColor: "#1e293b", border: "1px solid #334155", padding: "1.25rem", borderRadius: "8px" }}>
                  <span style={{ fontSize: "0.75rem", color: "#94a3b8", fontWeight: "700", letterSpacing: "0.05em" }}>PARALLEL RUNTIME</span>
                  <div style={{ fontSize: "2rem", fontWeight: "700", color: "#22c55e", margin: "0.5rem 0" }}>
                    {result.performance?.parallel_time_seconds || result.performance?.parallel || "N/A"}s
                  </div>
                  <small style={{ color: "#64748b" }}>Parallel execution across multiple cores</small>
                </div>

                <div style={{ backgroundColor: "#0c4a6e", border: "1px solid #0369a1", padding: "1.25rem", borderRadius: "8px" }}>
                  <span style={{ fontSize: "0.75rem", color: "#7dd3fc", fontWeight: "700", letterSpacing: "0.05em" }}>SPEED UP</span>
                  <div style={{ fontSize: "2.25rem", fontWeight: "800", color: "#38bdf8", margin: "0.25rem 0" }}>
                    {result.performance?.speedup_factor || result.performance?.speedup || "N/A"}x
                  </div>
                  <span style={{ fontSize: "0.8rem", color: "#7dd3fc" }}>Reduction in execution time using parallel vs serial</span>
                </div>

                <div style={{ backgroundColor: "#1e293b", border: "1px solid #334155", padding: "1.25rem", borderRadius: "8px" }}>
                  <span style={{ fontSize: "0.75rem", color: "#a855f7", fontWeight: "700", letterSpacing: "0.05em" }}>CORE EFFICIENCY</span>
                  <div style={{ fontSize: "2rem", fontWeight: "800", color: "#c084fc", margin: "0.5rem 0" }}>
                    {result.performance ? `${(((result.performance?.speedup_factor || result.performance?.speedup || 0) / 2) * 100).toFixed(1)}%` : "N/A"}
                  </div>
                  <small style={{ color: "#64748b" }}>Dual-core hardware utilization in VM</small>
                </div>

              </div>
            </div>
            {/* Predictions Content Block */}
            <div style={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px", padding: "1.5rem" }}>
              <h2 style={{ fontSize: "1.3rem", color: "#f1f5f9", margin: "0 0 1.25rem 0", fontWeight: "600", borderBottom: "1px solid #334155", paddingBottom: "0.5rem" }}>
                Target Projections ({result.prediction?.station_analyzed} - {result.prediction?.pollutant_target})
              </h2>
              
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "1.5rem" }}>
                <div style={{ backgroundColor: "#0f172a", padding: "1rem", borderRadius: "6px", border: "1px solid #1e293b" }}>
                  <span style={{ color: "#94a3b8", fontSize: "0.85rem", fontWeight: "600" }}>EXPECTED MEAN</span>
                  <div style={{ fontSize: "1.75rem", fontWeight: "700", color: "#38bdf8", marginTop: "0.25rem" }}>
                    {result.prediction?.expected_mean} ug/m³
                  </div>
                </div>

                <div style={{ backgroundColor: "#0f172a", padding: "1rem", borderRadius: "6px", border: "1px solid #1e293b" }}>
                  <span style={{ color: "#94a3b8", fontSize: "0.85rem", fontWeight: "600" }}>PERCENTILE 95 (p95)</span>
                  <div style={{ fontSize: "1.75rem", fontWeight: "700", color: "#fbbf24", marginTop: "0.25rem" }}>
                    {result.prediction?.p95_value} ug/m³
                  </div>
                </div>

                <div style={{ backgroundColor: "#0f172a", padding: "1rem", borderRadius: "6px", border: "1px solid #1e293b" }}>
                  <span style={{ color: "#94a3b8", fontSize: "0.85rem", fontWeight: "600" }}>WORST CASE (MAX)</span>
                  <div style={{ fontSize: "1.75rem", fontWeight: "700", color: "#f87171", marginTop: "0.25rem" }}>
                    {result.prediction?.max_value} ug/m³
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;