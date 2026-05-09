import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  Bot,
  Clock,
  FileText,
  Play,
  RefreshCw,
  ShoppingBag,
  Video,
  AlertTriangle,
  CheckCircle2,
  ExternalLink,
} from "lucide-react";
import { ACTIONS_URL, GITHUB_CONFIG } from "./config";
import { fetchTextFile, parseCsv, triggerWorkflow } from "./lib/github";
import "./styles.css";

function SaaSStyles() {
  return (
    <style>{`
      * { box-sizing: border-box; }

      body {
        margin: 0;
        background:
          radial-gradient(circle at top left, rgba(0, 210, 255, 0.20), transparent 35%),
          radial-gradient(circle at top right, rgba(170, 85, 255, 0.18), transparent 32%),
          linear-gradient(135deg, #050816 0%, #090d1f 45%, #050816 100%);
        color: #fff;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }

      .saas-shell {
        min-height: 100vh;
        padding: 24px;
      }

      .topbar {
        max-width: 1400px;
        margin: 0 auto 28px;
        padding: 18px 22px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(20px);
        border-radius: 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 30px 80px rgba(0,0,0,0.25);
      }

      .brand h1 {
        margin: 0;
        font-size: 25px;
        letter-spacing: -0.04em;
      }

      .brand p {
        margin: 5px 0 0;
        color: #94a3b8;
        font-size: 14px;
      }

      .top-actions {
        display: flex;
        gap: 12px;
        align-items: center;
      }

      .repo-pill {
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(0,0,0,0.20);
        padding: 10px 14px;
        border-radius: 999px;
        color: #cbd5e1;
        font-size: 13px;
      }

      .top-actions a {
        color: #67e8f9;
        text-decoration: none;
        display: flex;
        gap: 6px;
        align-items: center;
        font-size: 13px;
      }

      .hero-panel {
        max-width: 1400px;
        margin: 0 auto 24px;
        border-radius: 34px;
        padding: 34px;
        position: relative;
        overflow: hidden;
        background:
          linear-gradient(135deg, rgba(6,182,212,0.18), rgba(168,85,247,0.12)),
          rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 30px 90px rgba(0,0,0,0.30);
      }

      .hero-panel::after {
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        border-radius: 50%;
        right: -120px;
        top: -120px;
        background: rgba(34,211,238,0.18);
        filter: blur(20px);
      }

      .eyebrow {
        color: #67e8f9;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 12px;
        margin: 0 0 12px;
      }

      .hero-panel h2 {
        margin: 0;
        max-width: 760px;
        font-size: clamp(34px, 5vw, 64px);
        line-height: 0.96;
        letter-spacing: -0.065em;
      }

      .hero-panel p.subtitle {
        margin: 18px 0 0;
        max-width: 690px;
        color: #cbd5e1;
        font-size: 17px;
        line-height: 1.6;
      }

      .hero-actions {
        margin-top: 26px;
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
      }

      .primary-btn, .secondary-btn {
        border: 0;
        display: inline-flex;
        align-items: center;
        gap: 9px;
        padding: 13px 18px;
        border-radius: 18px;
        cursor: pointer;
        font-weight: 800;
        transition: 0.2s ease;
      }

      .primary-btn {
        background: linear-gradient(135deg, #22d3ee, #a78bfa);
        color: #020617;
        box-shadow: 0 14px 38px rgba(34,211,238,0.26);
      }

      .secondary-btn {
        color: #fff;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
      }

      .primary-btn:hover, .secondary-btn:hover {
        transform: translateY(-2px);
      }

      .dashboard-grid {
        max-width: 1400px;
        margin: 0 auto;
      }

      .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 18px;
        margin-bottom: 18px;
      }

      .metric-card, .panel {
        background: rgba(255,255,255,0.065);
        border: 1px solid rgba(255,255,255,0.10);
        backdrop-filter: blur(18px);
        border-radius: 28px;
        box-shadow: 0 24px 70px rgba(0,0,0,0.22);
      }

      .metric-card {
        padding: 22px;
        position: relative;
        overflow: hidden;
      }

      .metric-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(34,211,238,0.10), rgba(168,85,247,0.06));
        pointer-events: none;
      }

      .metric-content {
        position: relative;
        z-index: 1;
      }

      .metric-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .metric-icon {
        width: 46px;
        height: 46px;
        border-radius: 17px;
        display: grid;
        place-items: center;
        background: rgba(34,211,238,0.14);
        color: #67e8f9;
        border: 1px solid rgba(34,211,238,0.16);
      }

      .metric-card p {
        color: #94a3b8;
        margin: 0;
        font-size: 13px;
      }

      .metric-card h3 {
        margin: 16px 0 0;
        font-size: 38px;
        letter-spacing: -0.05em;
      }

      .metric-card small {
        display: block;
        margin-top: 9px;
        color: #67e8f9;
      }

      .content-grid {
        display: grid;
        grid-template-columns: 1.4fr 0.9fr;
        gap: 18px;
        margin-bottom: 18px;
      }

      .panel {
        padding: 24px;
      }

      .panel-title {
        display: flex;
        justify-content: space-between;
        gap: 18px;
        align-items: flex-start;
        margin-bottom: 20px;
      }

      .panel-title h3 {
        margin: 0;
        font-size: 23px;
        letter-spacing: -0.04em;
      }

      .panel-title p {
        margin: 5px 0 0;
        color: #94a3b8;
        font-size: 14px;
      }

      .status-pill {
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(16,185,129,0.14);
        border: 1px solid rgba(16,185,129,0.18);
        color: #34d399;
        font-size: 12px;
        font-weight: 800;
        white-space: nowrap;
      }

      .notice {
        max-width: 1400px;
        margin: 0 auto 18px;
        padding: 14px 16px;
        border-radius: 18px;
        background: rgba(245,158,11,0.14);
        border: 1px solid rgba(245,158,11,0.25);
        color: #fbbf24;
        display: flex;
        gap: 10px;
        align-items: center;
      }

      .token-box {
        display: grid;
        gap: 10px;
      }

      .token-box label {
        font-size: 13px;
        color: #cbd5e1;
        font-weight: 700;
      }

      .token-box input {
        width: 100%;
        padding: 14px 15px;
        border-radius: 16px;
        outline: none;
        color: #fff;
        background: rgba(0,0,0,0.22);
        border: 1px solid rgba(255,255,255,0.10);
      }

      .tiny {
        color: #64748b;
        margin: 0;
        font-size: 12px;
      }

      .button-row {
        display: flex;
        gap: 12px;
        margin-top: 16px;
        flex-wrap: wrap;
      }

      .detail-list {
        display: grid;
        gap: 12px;
      }

      .detail-item {
        display: flex;
        justify-content: space-between;
        gap: 14px;
        padding: 14px;
        border-radius: 18px;
        background: rgba(0,0,0,0.20);
        border: 1px solid rgba(255,255,255,0.06);
      }

      .detail-item span {
        color: #94a3b8;
        font-size: 13px;
      }

      .detail-item b {
        text-align: right;
        font-size: 13px;
        max-width: 58%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .badge-success {
        color: #34d399;
        background: rgba(16,185,129,0.14);
        border: 1px solid rgba(16,185,129,0.18);
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
      }

      .badge-neutral {
        color: #cbd5e1;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
      }

      .activity-list {
        display: grid;
        gap: 12px;
      }

      .activity-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        padding: 15px;
        background: rgba(0,0,0,0.22);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
      }

      .activity-row h4 {
        margin: 0;
        font-size: 14px;
      }

      .activity-row p {
        margin: 5px 0 0;
        font-size: 12px;
        color: #94a3b8;
      }

      .logs-box {
        height: 360px;
        overflow: auto;
        padding: 18px;
        border-radius: 20px;
        background: rgba(0,0,0,0.36);
        border: 1px solid rgba(255,255,255,0.07);
        color: #86efac;
        font-size: 12px;
        line-height: 1.65;
        white-space: pre-wrap;
      }

      .bottom-grid {
        display: grid;
        grid-template-columns: 0.9fr 1.1fr;
        gap: 18px;
      }

      .engine-list {
        display: grid;
        gap: 15px;
      }

      .engine-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .engine-status {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #34d399;
        font-size: 13px;
        font-weight: 700;
      }

      .pulse {
        width: 9px;
        height: 9px;
        border-radius: 999px;
        background: #34d399;
        box-shadow: 0 0 0 rgba(52,211,153,0.7);
        animation: pulse 1.6s infinite;
      }

      @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.45); }
        70% { box-shadow: 0 0 0 10px rgba(52,211,153,0); }
        100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
      }

      @media (max-width: 1000px) {
        .stats-grid, .content-grid, .bottom-grid {
          grid-template-columns: 1fr;
        }

        .topbar {
          flex-direction: column;
          align-items: flex-start;
          gap: 14px;
        }

        .top-actions {
          width: 100%;
          justify-content: space-between;
          flex-wrap: wrap;
        }

        .hero-panel {
          padding: 26px;
        }
      }
    `}</style>
  );
}

function MetricCard({ icon: Icon, label, value, hint }) {
  return (
    <div className="metric-card">
      <div className="metric-content">
        <div className="metric-top">
          <p>{label}</p>
          <div className="metric-icon">
            <Icon size={22} />
          </div>
        </div>
        <h3>{value}</h3>
        {hint && <small>{hint}</small>}
      </div>
    </div>
  );
}

function StatusBadge({ status }) {
  const ok =
    String(status || "").toLowerCase().includes("posted") ||
    String(status || "").toLowerCase().includes("success");

  return <span className={ok ? "badge-success" : "badge-neutral"}>{status || "Unknown"}</span>;
}

function App() {
  const [memoryRows, setMemoryRows] = useState([]);
  const [logs, setLogs] = useState("");
  const [runLock, setRunLock] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [token, setToken] = useState(localStorage.getItem("github_pat") || "");

  const latest = memoryRows[memoryRows.length - 1] || {};
  const latestFive = memoryRows.slice(-5).reverse();
  const successfulPosts = memoryRows.filter((r) =>
    String(r.status || "").toLowerCase().includes("posted")
  ).length;

  const totalReels = memoryRows.filter((r) => r.reel_id).length;

  const lastLogLines = useMemo(
    () => logs.split(/\r?\n/).filter(Boolean).slice(-90).reverse(),
    [logs]
  );

  const latestLog = lastLogLines[0] || "No recent activity";

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

      const errors = [memoryText, logText, lockText].filter((x) => x.status === "rejected");
      if (errors.length) {
        setMessage(
          "Some files could not be loaded. Check config.js repo settings and repository visibility."
        );
      }
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

  useEffect(() => {
    loadData();
  }, []);

  return (
    <>
      <SaaSStyles />

      <div className="saas-shell">
        <header className="topbar">
          <div className="brand">
            <h1>Nooraxo AI Commerce Engine</h1>
            <p>AI-powered Facebook post, reel, voiceover and sales automation</p>
          </div>

          <div className="top-actions">
            <div className="repo-pill">
              {GITHUB_CONFIG.OWNER}/{GITHUB_CONFIG.REPO}
            </div>
            <a href={ACTIONS_URL} target="_blank" rel="noreferrer">
              Open GitHub Actions <ExternalLink size={14} />
            </a>
          </div>
        </header>

        <section className="hero-panel">
  <p className="eyebrow">AI Facebook Commerce Platform</p>

  <h2>
    Automate Facebook posts, AI reels, captions & voiceovers.
  </h2>

  <p className="subtitle">
    🚀 Smart Posting &nbsp; • &nbsp;
    🎬 Viral AI Reels &nbsp; • &nbsp;
    🎤 Human-like Voiceovers &nbsp; • &nbsp;
    📈 Growth Automation
    <br /><br />
    Want this automation for your business?
    <br />
    📱 WhatsApp: 03169250202
  </p>

  <div className="hero-actions">
    <button className="primary-btn" onClick={handleRun}>
      <Play size={18} /> Run Automation
    </button>

    <button className="secondary-btn" onClick={loadData}>
      <RefreshCw size={18} /> Refresh Dashboard
    </button>
  </div>
</section>

        {message && (
          <div className="notice">
            <AlertTriangle size={18} />
            {message}
          </div>
        )}

        <main className="dashboard-grid">
          <section className="stats-grid">
            <MetricCard
              icon={ShoppingBag}
              label="Total Published"
              value={successfulPosts}
              hint="from memory.csv"
            />
            <MetricCard
              icon={Video}
              label="Reels Published"
              value={totalReels}
              hint={latest.reel_id ? "latest reel active" : "no reel found"}
            />
            <MetricCard
              icon={Bot}
              label="AI Category"
              value={latest.category || "—"}
              hint={latest.hook_style || "local AI style"}
            />
            <MetricCard
              icon={Clock}
              label="Last Run Lock"
              value={runLock || "—"}
              hint="automation run state"
            />
          </section>

          <section className="content-grid">
            <div className="panel">
              <div className="panel-title">
                <div>
                  <h3>Run Automation</h3>
                  <p>Trigger your GitHub Actions workflow manually from the dashboard.</p>
                </div>
                <span className="status-pill">System Online</span>
              </div>

              <div className="token-box">
                <label>GitHub Personal Access Token</label>
                <input
                  type="password"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  placeholder="Paste PAT with Actions permission"
                />
                <p className="tiny">
                  Admin use only. Token is stored locally in your browser, not in repository files.
                </p>
              </div>

              <div className="button-row">
                <button className="primary-btn" onClick={handleRun}>
                  <Play size={18} /> Run Now
                </button>
                <button className="secondary-btn" onClick={loadData}>
                  <RefreshCw size={18} /> Refresh
                </button>
              </div>
            </div>

            <div className="panel">
              <div className="panel-title">
                <div>
                  <h3>Latest Published Product</h3>
                  <p>Latest commerce result from memory.csv</p>
                </div>
                <CheckCircle2 color="#34d399" />
              </div>

              <div className="detail-list">
                <div className="detail-item">
                  <span>Product ID</span>
                  <b>{latest.product_id || "—"}</b>
                </div>
                <div className="detail-item">
                  <span>Status</span>
                  <StatusBadge status={latest.status} />
                </div>
                <div className="detail-item">
                  <span>Price</span>
                  <b>{latest.price ? `Rs ${latest.price}` : "—"}</b>
                </div>
                <div className="detail-item">
                  <span>Caption Style</span>
                  <b>{latest.caption_style || "—"}</b>
                </div>
                <div className="detail-item">
                  <span>Music</span>
                  <b>{latest.music_url || "—"}</b>
                </div>
                <div className="detail-item">
                  <span>Date</span>
                  <b>{latest.date || "—"}</b>
                </div>
              </div>
            </div>
          </section>

          <section className="bottom-grid">
            <div className="panel">
              <div className="panel-title">
                <div>
                  <h3>AI Engine Health</h3>
                  <p>Core system modules status</p>
                </div>
              </div>

              <div className="engine-list">
                {[
                  ["Facebook Publishing", "Ready"],
                  ["AI Caption Engine", "Active"],
                  ["Reel Generator", "Active"],
                  ["Voiceover Engine", "Configured"],
                  ["Music Engine", "Active"],
                ].map((item) => (
                  <div className="engine-row" key={item[0]}>
                    <span>{item[0]}</span>
                    <div className="engine-status">
                      <span className="pulse" />
                      {item[1]}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel">
              <div className="panel-title">
                <div>
                  <h3>Automation Activity</h3>
                  <p>Latest execution summary</p>
                </div>
                <span className="status-pill">{loading ? "Loading" : "Live"}</span>
              </div>

              <div className="activity-list">
                <div className="activity-row">
                  <div>
                    <h4>Latest Log</h4>
                    <p>{latestLog}</p>
                  </div>
                  <Activity color="#67e8f9" />
                </div>
                <div className="activity-row">
                  <div>
                    <h4>Last Reel ID</h4>
                    <p>{latest.reel_id || "No reel ID found yet"}</p>
                  </div>
                  <Video color="#a78bfa" />
                </div>
                <div className="activity-row">
                  <div>
                    <h4>Last AI Hook</h4>
                    <p>{latest.hook_style || "No hook style found yet"}</p>
                  </div>
                  <Bot color="#34d399" />
                </div>
              </div>
            </div>
          </section>

          <section className="panel" style={{ marginTop: 18 }}>
  <div className="panel-title">
    <div>
      <h3>Latest 5 Posts & Reels</h3>
      <p>Direct links to recently published Facebook content</p>
    </div>
    <ExternalLink color="#67e8f9" />
  </div>

  <div className="activity-list">
    {latestFive.length ? (
      latestFive.map((item, index) => (
        <div className="activity-row" key={index}>
          <div>
            <h4>{item.product_id || `Post ${index + 1}`}</h4>
            <p>{item.date || "No date found"}</p>
          </div>

          <div className="button-row" style={{ marginTop: 0 }}>
            {item.post_url && (
              <a
                className="secondary-btn"
                href={item.post_url}
                target="_blank"
                rel="noreferrer"
              >
                View Post <ExternalLink size={14} />
              </a>
            )}

            {(item.reel_url || item.reel_id) && (
              <a
                className="primary-btn"
                href={item.reel_url || `https://facebook.com/${item.reel_id}`}
                target="_blank"
                rel="noreferrer"
              >
                View Reel <ExternalLink size={14} />
              </a>
            )}
          </div>
        </div>
      ))
    ) : (
      <p className="tiny">No published posts found yet.</p>
    )}
  </div>
</section>
          <section className="panel" style={{ marginTop: 18 }}>
            <div className="panel-title">
              <div>
                <h3>Logs Viewer</h3>
                <p>Latest entries from run_log.txt</p>
              </div>
              <FileText color="#67e8f9" />
            </div>

            <pre className="logs-box">
              {loading ? "Loading logs..." : lastLogLines.join("\n") || "No logs found."}
            </pre>
          </section>
        </main>
      </div>
    </>
  );
}

createRoot(document.getElementById("root")).render(<App />);
