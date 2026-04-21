import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");

  const [prompt, setPrompt] = useState("");
  const [modelName, setModelName] = useState("gpt-4o-mini");

  const [response, setResponse] = useState(null);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState("");

  const API = "http://127.0.0.1:8000";

  const login = async () => {
    try {
      setError("");
      const res = await axios.post(
        `${API}/auth/login`,
        {
          email: email,
          password: password,
        }
      );

      setToken(res.data.access_token);
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    }
  };


  const fetchLogs = async () => {
    if (!token) return;
    try {
      setError("");
      const res = await axios.get(`${API}/admin/logs`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setLogs(res.data);
    } catch (err) {
      setLogs([]);
      setError(err?.response?.data?.detail || "Failed to fetch logs");
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [token]);

  const handleSubmit = async () => {
    try {
      setError("");
      const res = await axios.post(
        `${API}/employee/generate`,
        {
          prompt: prompt,
          model_name: modelName,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setResponse(res.data);
      fetchLogs();
    } catch (err) {
      setError(err?.response?.data?.detail || "Request failed");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>AI Observability Dashboard</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {!token && (
        <>
          <h2>Login</h2>
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <br /><br />
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <br /><br />
          <button onClick={login}>Login</button>
          <hr />
        </>
      )}

      {token && (
        <>
          <h2>Send Prompt</h2>

          <select
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
          >
            <option value="gpt-4o-mini">gpt-4o-mini</option>
            <option value="gpt-4o">gpt-4o</option>
          </select>

          <br /><br />

          <textarea
            placeholder="Enter prompt..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows="4"
            cols="50"
          />

          <br /><br />

          <button onClick={handleSubmit}>Generate</button>

          {response && (
            <div style={{ marginTop: "20px" }}>
              <h3>Latest Response</h3>
              <p>{response.response}</p>
              <p>Cost: ${response.cost}</p>
              <p>Latency: {response.latency}s</p>
              <p>Drift: {response.drift_score}</p>
            </div>
          )}

          <hr style={{ margin: "40px 0" }} />

          <h2>Cost Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={logs}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="created_at" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="cost" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>

          <h2>Latency Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={logs}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="created_at" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="latency" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>

          <hr style={{ margin: "40px 0" }} />

          <h2>Request History</h2>
          <table border="1" cellPadding="8">
            <thead>
              <tr>
                <th>User</th>
                <th>Cost</th>
                <th>Latency</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, index) => (
                <tr key={index}>
                  <td>{log.user_id}</td>
                  <td>${log.cost}</td>
                  <td>{log.latency}s</td>
                  <td>
                    {new Date(log.created_at).toLocaleTimeString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

export default App;
