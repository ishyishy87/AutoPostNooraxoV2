import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { Activity, Bot, Clock, FileText, Play, RefreshCw, ShoppingBag, Video, AlertTriangle, CheckCircle2, ExternalLink } from "lucide-react";
import { ACTIONS_URL, GITHUB_CONFIG } from "./config";
import { fetchTextFile, parseCsv, triggerWorkflow } from "./lib/github";
import "./styles.css";

function StatCard({ icon: Icon, label, value, hint }) {
  return (
    <div className="card stat-card">
      <div className="stat-icon"><Icon size={22} /></div>
      <div>
        <p className="muted">{label}</p>
        <h2>{value}</h2>
        {hint && <small>{hint}</small>}
      </div>
    </div>
  );
}

function StatusBadge({ status }) {
  const ok = String(status || "").toLowerCase().includes("posted") || String(status || "").toLowerCase().includes("success");
  return <span className={ok ? "badge success" : "badge"}>{status || "Unknown"}</span>;
}

function App() {
  const [memoryRows, setMemoryRows] = useState([]);
  const [logs, setLogs] = useState("");
  const [runLock, setRunLock] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [token, setToken] = useState(localStorage.getItem("github_pat") || "");

  const latest = memoryRows[memoryRows.length - 1] || {};
  const successfulPosts = memoryRows.filter(r => String(r.status || "").toLowerCase().includes("posted")).length;
  const lastLogLines = useMemo(() => logs.split(/\r?\n/).filter(Boolean).slice(-80).reverse(), [logs]);

  async function loadData() {
    setLoading(true);
    setMessage("");
    try {
      const [memoryText, logText, lockText] = await Promise.allSettled([
        fetchTextFile("memory.csv"),
        fetchTextFile("run_log.txt"),
        fetchTextFile("run_lock.txt"),
      ]);

      if (memoryText.status === "fulfilled") setMemoryRows(parseCsv(memoryText.value));
      if (logText.status === "fulfilled") setLogs(logText.value);
      if (lockText.status === "fulfilled") setRunLock(lockText.value.trim());

      const errors = [memoryText, logText, lockText].filter(x => x.status === "rejected");
      if (errors.length) setMessage("Some files could not be loaded. Check config.js repo settings and repository visibility.");
    } catch (e) {
      setMessage(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleRun() {
    setMessage("");
    try {
      if (token) localStorage.setItem("github_pat", token);
      await triggerWorkflow(token);
      setMessage("Automation workflow triggered successfully. Refresh logs after a few minutes.");
    } catch (e) {
      setMessage(e.message);
    }
  }

  useEffect(() => { loadData(); }, []);

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">AI Facebook Commerce Automation</p>
          <h1>AutoPostNooraxoV2 Dashboard</h1>
          <p className="subtitle">Monitor posts, reels, AI content, logs, and manually trigger automation.</p>
        </div>
        <div className="repo-box">
          <span>{GITHUB_CONFIG.OWNER}/{GITHUB_CONFIG.REPO}</span>
          <a href={ACTIONS_URL} target="_blank" rel="noreferrer">Open Actions <ExternalLink size={14}/></a>
        </div>
      </header>

      {message && <div className="notice"><AlertTriangle size={18}/>{message}</div>}

      <section className="grid stats-grid">
        <StatCard icon={ShoppingBag} label="Total Published" value={successfulPosts} hint="from memory.csv" />
        <StatCard icon={Video} label="Last Reel ID" value={latest.reel_id || "—"} hint="latest successful run" />
        <StatCard icon={Bot} label="Last Category" value={latest.category || "—"} hint={latest.hook_style || "AI style"} />
        <StatCard icon={Clock} label="Run Lock" value={runLock || "—"} hint="last run date" />
      </section>

      <main className="main-grid">
        <section className="card run-card">
          <div className="section-title">
            <Activity />
            <div>
              <h2>Run Automation</h2>
              <p>Trigger the GitHub Actions workflow manually.</p>
            </div>
          </div>

          <label>GitHub Personal Access Token</label>
          <input
            type="password"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            placeholder="Paste PAT with Actions permission"
          />
          <p className="tiny-warning">For admin use only. Token is stored locally in your browser, not in the repo.</p>

          <div className="button-row">
            <button onClick={handleRun}><Play size={18}/> Run Now</button>
            <button className="secondary" onClick={loadData}><RefreshCw size={18}/> Refresh</button>
          </div>
        </section>

        <section className="card latest-card">
          <div className="section-title">
            <CheckCircle2 />
            <div>
              <h2>Latest Published Product</h2>
              <p>Summary from memory.csv</p>
            </div>
          </div>
          <div className="detail-list">
            <div><span>Product ID</span><b>{latest.product_id || "—"}</b></div>
            <div><span>Status</span><StatusBadge status={latest.status} /></div>
            <div><span>Price</span><b>{latest.price ? `Rs ${latest.price}` : "—"}</b></div>
            <div><span>Caption Style</span><b>{latest.caption_style || "—"}</b></div>
            <div><span>Music</span><b className="truncate">{latest.music_url || "—"}</b></div>
            <div><span>Date</span><b>{latest.date || "—"}</b></div>
          </div>
        </section>
      </main>

      <section className="card logs-card">
        <div className="section-title">
          <FileText />
          <div>
            <h2>Logs Viewer</h2>
            <p>Latest entries from run_log.txt</p>
          </div>
        </div>
        {loading ? <p>Loading...</p> : <pre>{lastLogLines.join("\n") || "No logs found."}</pre>}
      </section>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
