import { GITHUB_CONFIG, RAW_BASE_URL } from "../config";

export async function fetchTextFile(fileName) {
  const url = `${RAW_BASE_URL}/${fileName}?t=${Date.now()}`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`Could not load ${fileName}. HTTP ${res.status}`);
  return await res.text();
}

export function parseCsv(csvText) {
  const lines = csvText.trim().split(/\r?\n/);
  if (!lines.length) return [];
  const headers = splitCsvLine(lines[0]);
  return lines.slice(1).filter(Boolean).map(line => {
    const values = splitCsvLine(line);
    const row = {};
    headers.forEach((h, i) => row[h] = values[i] ?? "");
    return row;
  });
}

function splitCsvLine(line) {
  const result = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    const next = line[i + 1];
    if (ch === '"' && inQuotes && next === '"') {
      current += '"';
      i++;
    } else if (ch === '"') {
      inQuotes = !inQuotes;
    } else if (ch === ',' && !inQuotes) {
      result.push(current);
      current = "";
    } else {
      current += ch;
    }
  }
  result.push(current);
  return result;
}

export async function triggerWorkflow(token) {
  if (!token) throw new Error("GitHub token is required to trigger workflow from dashboard.");

  const url = `https://api.github.com/repos/${GITHUB_CONFIG.OWNER}/${GITHUB_CONFIG.REPO}/actions/workflows/${GITHUB_CONFIG.WORKFLOW_FILE}/dispatches`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ ref: GITHUB_CONFIG.BRANCH })
  });

  if (res.status !== 204) {
    const text = await res.text();
    throw new Error(`Workflow trigger failed. HTTP ${res.status}. ${text}`);
  }
  return true;
}
