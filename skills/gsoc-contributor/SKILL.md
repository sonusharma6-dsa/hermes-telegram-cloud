---
name: gsoc-contributor
description: Autonomously find open issues in target GSoC / open-source repositories, clone the repo, fix bugs/add features, run tests, and submit clean Pull Requests (PRs).
---

# Autonomous GSoC & Open-Source Contributor Skill

When a user asks to contribute to a GSoC project, find good-first-issues, or submit a PR for a repository (e.g. `/gsoc <repo_url>` or "Contribute to <repo>"):

Follow this 5-step autonomous GitHub contribution workflow:

### Step 1: Scan & Find Target Issues
- Run `gh issue list --repo <owner/repo> --label "good-first-issue,help wanted" --state open`
- Select an open, unassigned bug report or feature request.
- Read issue details and requirements using `gh issue view <issue_number> --repo <owner/repo>`.

### Step 2: Fork & Clone Repository
- Fork the target repository: `gh repo fork <owner/repo> --clone=true`
- Checkout a clean working feature branch: `git checkout -b fix-issue-<issue_number>`

### Step 3: Reproduce & Edit Code
- Locate relevant files and reproduce test cases.
- Write clean, documented code fixing the bug or adding the feature.
- Ensure all existing unit tests and linters pass (`npm test`, `pytest`, `cargo test`, etc.).

### Step 4: Commit & Push
- Add changes: `git add .`
- Create a clear, semantic commit message: `git commit -m "fix(#issue): resolve <issue summary>"`
- Push branch to fork: `git push -u origin fix-issue-<issue_number>`

### Step 5: Submit Pull Request (PR)
- Submit PR to original upstream repo:
  `gh pr create --repo <owner/repo> --title "fix: <summary>" --body "Closes #<issue_number>. <Detailed explanation of fix and tests.>"`
- Report the live Pull Request link back to the user in Telegram!
