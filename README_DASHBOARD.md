# AutoPostNooraxoV2 Dashboard

This package adds a first-version GUI dashboard for your Facebook automation system.

## Features

- Dashboard stats from `memory.csv`
- Latest product/reel status
- Logs viewer from `run_log.txt`
- Run Automation button for GitHub Actions workflow dispatch
- GitHub Pages deployment workflow

## Install

Copy the following into your repository root:

```text
dashboard/
.github/workflows/deploy-dashboard.yml
```

## Configure

Edit:

```text
dashboard/src/config.js
```

Update:

```js
OWNER: "YOUR_GITHUB_USERNAME",
REPO: "AutoPostNooraxoV2",
BRANCH: "main",
WORKFLOW_FILE: "run.yml",
```

`WORKFLOW_FILE` must match your workflow filename inside `.github/workflows/`.

## Deploy to GitHub Pages

1. Push changes to GitHub.
2. Go to repository Settings → Pages.
3. Source should be GitHub Actions.
4. Run `Deploy Dashboard` workflow.

## Run Automation Button

The dashboard can trigger your workflow using a GitHub Personal Access Token entered in the browser.

For security, use only for admin/private dashboard access. The token is stored only in browser localStorage.

Recommended token permissions:

- Actions: read/write
- Contents: read

## Safer commercial version

For selling to customers, the safer architecture is:

- Frontend dashboard on GitHub Pages
- Backend/API on Render, Railway, or Cloudflare Workers
- Tokens stored server-side, not browser-side
