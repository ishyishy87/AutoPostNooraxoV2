import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bot,
  CalendarDays,
  CheckCircle2,
  Clock,
  ExternalLink,
  Eye,
  FileText,
  Flame,
  Heart,
  MessageCircle,
  Play,
  RefreshCw,
  Rocket,
  Send,
  Share2,
  ShieldCheck,
  ShoppingBag,
  Sparkles,
  TrendingUp,
  Video,
  Zap,
} from "lucide-react";
import { ACTIONS_URL, GITHUB_CONFIG } from "./config";
import { fetchTextFile, parseCsv, triggerWorkflow } from "./lib/github";
import "./styles.css";

const FILTER_DAYS = [1, 2, 3, 4, 5, 6, 7];

function toNumber(value) {
  const n = Number(value || 0);
  return Number.isFinite(n) ? n : 0;
}

function formatNumber(value) {
  return new Intl.NumberFormat("en-PK").format(toNumber(value));
}

function parseDate(value) {
  if (!value) return null;
  const raw = String(value).trim();
  if (!raw) return null;

  const normalized = raw.replace(" ", "T");
  const direct = new Date(normalized);
  if (!Number.isNaN(direct.getTime())) return direct;

  const fallback = new Date(raw);
  if (!Number.isNaN(fallback.getTime())) return fallback;

  return null;
}

function getRowDate(row) {
  return parseDate(row.analytics_updated_at) || parseDate(row.date);
}

function withinLastDays(row, days) {
  const d = getRowDate(row);
  if (!d) return true;
  const now = new Date();
  const cutoff = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
  return d >= cutoff;
}

function getPostId(row) {
  const postUrl = String(row.post_url || "").trim();
  if (!postUrl) return "";
  return postUrl.split("facebook.com/").pop() || "";
}

function safeUrl(url) {
  const value = String(url || "").trim();
  if (!value || value.toLowerCase() === "nan") return "";
  return value;
}

function MetricCard({ icon: Icon, label, value, hint, tone = "cyan" }) {
  return (
    <div className={`metric-card tone-${tone}`}>
      <div className="metric-glow" />
      <div className="metric-top">
        <div>
          <p>{label}</p>
          <h3>{value}</h3>
        </div>
        <div className="metric-icon">
          <Icon size={21} />
        </div>
      </div>
      {hint && <span>{hint}</span>}
    </div>
  );
}

function StatusBadge({ status }) {
  const text = String(status || "Unknown");
  const ok = text.toLowerCase().includes("posted") || text.toLowerCase().includes("success");
  return <span className={ok ? "badge badge-success" : "badge badge-muted"}>{text}</span>;
}

function FilterButton({ days, active, onClick }) {
  return (
    <button className={active ? "filter-chip active" : "filter-chip"} onClick={onClick}>
      {days}D
    </button>
  );
}

function SectionTitle({ icon: Icon, title, subtitle, right }) {
  return (
    <div className="section-title">
      <div className="section-title-left">
        <div className="section-icon">
          <Icon size={20} />
        </div>
        <div>
          <h2>{title}</h2>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
      {right}
    </div>
  );
}

function LinkButton({ href, children, variant = "secondary" }) {
  if (!href) return null;
  return (
    <a className={`link-btn ${variant}`} href={href} target="_blank" rel="noreferrer">
      {children} <ExternalLink size={14} />
    </a>
  );
}

function App() {
  const [memoryRows, setMemoryRows] = useState([]);
  const [logs, setLogs] = useState("");
  const [runLock, setRunLock] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [token, setToken] = useState(localStorage.getItem("github_pat") || "");
  const [dayFilter, setDayFilter] = useState(7);

  const latest = memoryRows[memoryRows.length - 1] || {};

  const filteredRows = useMemo(() => {
    const rows = memoryRows.filter((row) => withinLastDays(row, dayFilter));
    return rows.length ? rows : memoryRows.slice(-Math.min(memoryRows.length, 21));
  }, [memoryRows, dayFilter]);

  const analytics = useMemo(() => {
    const totalPosts = filteredRows.filter((r) => String(r.status || "").toLowerCase().includes("posted")).length;
    const totalReels = filteredRows.filter((r) => String(r.reel_id || "").trim()).length;
    const totalLikes = filteredRows.reduce((sum, r) => sum + toNumber(r.likes) + toNumber(r.reel_likes), 0);
    const totalComments = filteredRows.reduce((sum, r) => sum + toNumber(r.comments) + toNumber(r.reel_comments), 0);
    const totalShares = filteredRows.reduce((sum, r) => sum + toNumber(r.shares), 0);
    const totalViews = filteredRows.reduce((sum, r) => sum + toNumber(r.reel_views), 0);
    const totalScore = filteredRows.reduce((sum, r) => sum + toNumber(r.engagement_score), 0);

    const bestPost = [...filteredRows].sort((a, b) => toNumber(b.engagement_score) - toNumber(a.engagement_score))[0] || {};
    const bestReel = [...filteredRows].sort((a, b) => toNumber(b.reel_views) - toNumber(a.reel_views))[0] || {};

    const avgEngagement = totalPosts || totalReels ? Math.round(totalScore / Math.max(filteredRows.length, 1)) : 0;

    return {
      totalPosts,
      totalReels,
      totalLikes,
      totalComments,
      totalShares,
      totalViews,
      totalScore,
      avgEngagement,
      bestPost,
      bestReel,
    };
  }, [filteredRows]);

  const latestFive = useMemo(() => filteredRows.slice(-5).reverse(), [filteredRows]);

  const lastLogLines = useMemo(
    () => logs.split(/\r?\n/).filter(Boolean).slice(-90).reverse(),
    [logs]
  );

  const latestLog = lastLogLines[0] || "No recent activity found yet.";

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
        setMessage("Some files could not be loaded. Check dashboard config.js and repository visibility.");
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
    <div className="app-shell">
      <header className="mobile-header">
        <div>
          <p>AI Commerce</p>
          <h1>Nooraxo Engine</h1>
        </div>
        <button className="icon-button" onClick={loadData} aria-label="Refresh dashboard">
          <RefreshCw size={18} />
        </button>
      </header>

      <main className="dashboard-wrap">
        <section className="hero-card">
          <div className="hero-content">
            <div className="hero-badge">
              <Sparkles size={15} /> AI Social Commerce SaaS
            </div>
            <h1>Executive analytics for AI-powered Facebook sales automation.</h1>
            <p>
              Track posts, reels, views, comments, shares, engagement score and automation health from one premium mobile-ready dashboard.
            </p>
            <div className="hero-actions">
              <button className="primary-btn" onClick={handleRun}>
                <Play size={18} /> Run Automation
              </button>
              <button className="secondary-btn" onClick={loadData}>
                <RefreshCw size={18} /> Refresh
              </button>
            </div>
          </div>
          <div className="hero-side">
            <div className="live-pill"><span /> Live Analytics</div>
            <div className="hero-score">
              <p>Engagement Score</p>
              <strong>{formatNumber(analytics.totalScore)}</strong>
              <small>Last {dayFilter} day{dayFilter > 1 ? "s" : ""}</small>
            </div>
          </div>
        </section>

        <section className="filter-panel">
          <div>
            <h2>Performance Window</h2>
            <p>Filter dashboard analytics from last 1 to 7 days.</p>
          </div>
          <div className="filter-row">
            {FILTER_DAYS.map((d) => (
              <FilterButton key={d} days={d} active={dayFilter === d} onClick={() => setDayFilter(d)} />
            ))}
          </div>
        </section>

        {message && (
          <div className="notice">
            <AlertTriangle size={18} />
            <span>{message}</span>
          </div>
        )}

        <section className="metrics-grid">
          <MetricCard icon={ShoppingBag} label="Posts" value={formatNumber(analytics.totalPosts)} hint="published in selected period" tone="cyan" />
          <MetricCard icon={Video} label="Reels" value={formatNumber(analytics.totalReels)} hint="AI videos published" tone="purple" />
          <MetricCard icon={Eye} label="Reel Views" value={formatNumber(analytics.totalViews)} hint="plays from analytics worker" tone="blue" />
          <MetricCard icon={Heart} label="Likes" value={formatNumber(analytics.totalLikes)} hint="post + reel reactions" tone="pink" />
          <MetricCard icon={MessageCircle} label="Comments" value={formatNumber(analytics.totalComments)} hint="post + reel comments" tone="green" />
          <MetricCard icon={Share2} label="Shares" value={formatNumber(analytics.totalShares)} hint="Facebook shares" tone="orange" />
          <MetricCard icon={TrendingUp} label="AI Score" value={formatNumber(analytics.totalScore)} hint="weighted engagement" tone="lime" />
          <MetricCard icon={Clock} label="Run Lock" value={runLock || "—"} hint="latest automation run" tone="slate" />
        </section>

        <section className="executive-grid">
          <div className="panel main-panel">
            <SectionTitle
              icon={BarChart3}
              title="AI Analytics Summary"
              subtitle="Best content and campaign performance in the selected period."
              right={<span className="status-pill">{filteredRows.length} records</span>}
            />

            <div className="insight-grid">
              <div className="insight-card winner">
                <Flame size={22} />
                <div>
                  <p>Best Performing Product</p>
                  <h3>{analytics.bestPost.product_id || "—"}</h3>
                  <span>Score: {formatNumber(analytics.bestPost.engagement_score || 0)}</span>
                </div>
              </div>

              <div className="insight-card">
                <Video size={22} />
                <div>
                  <p>Best Reel by Views</p>
                  <h3>{analytics.bestReel.product_id || "—"}</h3>
                  <span>{formatNumber(analytics.bestReel.reel_views || 0)} plays</span>
                </div>
              </div>

              <div className="insight-card">
                <Zap size={22} />
                <div>
                  <p>Avg Engagement</p>
                  <h3>{formatNumber(analytics.avgEngagement)}</h3>
                  <span>per memory row</span>
                </div>
              </div>
            </div>

            <div className="latest-box">
              <h3>Latest 5 Posts & Reels</h3>
              <div className="latest-list">
                {latestFive.length ? latestFive.map((item, index) => {
                  const postUrl = safeUrl(item.post_url);
                  const reelUrl = safeUrl(item.reel_url) || (item.reel_id ? `https://facebook.com/${item.reel_id}` : "");
                  return (
                    <div className="latest-row" key={`${item.product_id}-${index}`}>
                      <div className="latest-main">
                        <div className="latest-icon"><Rocket size={17} /></div>
                        <div>
                          <h4>{item.product_id || `Content ${index + 1}`}</h4>
                          <p>{item.date || item.analytics_updated_at || "No date found"}</p>
                        </div>
                      </div>
                      <div className="latest-actions">
                        <LinkButton href={postUrl}>Post</LinkButton>
                        <LinkButton href={reelUrl} variant="primary">Reel</LinkButton>
                      </div>
                    </div>
                  );
                }) : <p className="empty-text">No published content found for this period.</p>}
              </div>
            </div>
          </div>

          <aside className="panel side-panel">
            <SectionTitle icon={ShieldCheck} title="AI Engine Health" subtitle="Core modules status" />
            <div className="health-list">
              {[
                ["Facebook Publishing", "Operational", Send],
                ["Reel Generator", "Active", Video],
                ["Voiceover Engine", "Ready", Bot],
                ["Comment AI", "Tracking", MessageCircle],
                ["Analytics Worker", "Enabled", Activity],
              ].map(([name, status, Icon]) => (
                <div className="health-row" key={name}>
                  <div><Icon size={17} /><span>{name}</span></div>
                  <b><i />{status}</b>
                </div>
              ))}
            </div>

            <div className="latest-product">
              <h3>Latest Published</h3>
              <div className="detail-row"><span>Product</span><b>{latest.product_id || "—"}</b></div>
              <div className="detail-row"><span>Status</span><StatusBadge status={latest.status} /></div>
              <div className="detail-row"><span>Price</span><b>{latest.price ? `Rs ${latest.price}` : "—"}</b></div>
              <div className="detail-row"><span>Category</span><b>{latest.category || "—"}</b></div>
              <div className="detail-row"><span>Updated</span><b>{latest.analytics_updated_at || latest.date || "—"}</b></div>
            </div>
          </aside>
        </section>

        <section className="panel run-panel">
          <SectionTitle icon={Play} title="Run Automation" subtitle="Trigger GitHub Actions manually from dashboard." />
          <div className="token-grid">
            <div>
              <label>GitHub Personal Access Token</label>
              <input
                type="password"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Paste PAT with Actions permission"
              />
              <p>Stored only in your browser local storage.</p>
            </div>
            <div className="run-buttons">
              <button className="primary-btn" onClick={handleRun}><Play size={18} /> Run Now</button>
              <button className="secondary-btn" onClick={loadData}><RefreshCw size={18} /> Refresh</button>
              <a className="ghost-link" href={ACTIONS_URL} target="_blank" rel="noreferrer">Open Actions <ExternalLink size={14} /></a>
            </div>
          </div>
        </section>

        <section className="panel logs-panel">
          <SectionTitle
            icon={FileText}
            title="Automation Logs"
            subtitle="Latest entries from run_log.txt"
            right={<span className="status-pill">{loading ? "Loading" : "Live"}</span>}
          />
          <div className="log-highlight">
            <Activity size={17} /> {latestLog}
          </div>
          <pre>{loading ? "Loading logs..." : lastLogLines.join("\n") || "No logs found."}</pre>
        </section>

        <footer className="dashboard-footer">
          <span>{GITHUB_CONFIG.OWNER}/{GITHUB_CONFIG.REPO}</span>
          <span>AI Commerce Automation Dashboard</span>
        </footer>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
