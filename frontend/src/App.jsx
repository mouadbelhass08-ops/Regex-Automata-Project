import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function App() {
  const [status, setStatus] = useState("checking...");

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("unreachable"));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>Regex Automata</h1>
      <p>
        Backend status: <strong>{status}</strong>
      </p>
    </main>
  );
}
