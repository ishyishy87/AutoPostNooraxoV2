// Update these values before deploying to GitHub Pages.
// Example:
// OWNER: "your-github-username"
// REPO: "AutoPostNooraxoV2"
// BRANCH: "main"
// WORKFLOW_FILE: "run.yml" or "autopost.yml"

export const GITHUB_CONFIG = {
  OWNER: "ishyishy87",
  REPO: "AutoPostNooraxoV2",
  BRANCH: "main",
  WORKFLOW_FILE: "run.yml",
};

export const RAW_BASE_URL = `https://raw.githubusercontent.com/${GITHUB_CONFIG.OWNER}/${GITHUB_CONFIG.REPO}/${GITHUB_CONFIG.BRANCH}`;
export const ACTIONS_URL = `https://github.com/${GITHUB_CONFIG.OWNER}/${GITHUB_CONFIG.REPO}/actions/workflows/${GITHUB_CONFIG.WORKFLOW_FILE}`;
