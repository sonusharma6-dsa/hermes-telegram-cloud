---
name: gsoc-contributor
description: Autonomously find or CREATE open issues in target GSoC / open-source repositories, clone repos, fix bugs/add features, run tests, and submit clean Pull Requests (PRs).
---

# Autonomous GSoC & Open-Source Contributor Skill

When a user asks to contribute to a GSoC project, create an issue, find good-first-issues, or submit a PR for a repository (e.g. `/gsoc <repo_url>` or "Create an issue in <repo>" or "Contribute to <repo>"):

Follow this autonomous GitHub workflow:

### Capability 1: Create & Open New Issues
- To open a new issue for a bug, feature request, or security/code flaw:
  `gh issue create --repo <owner/repo> --title "<clear title>" --body "<detailed reproduction steps or feature proposal>" --label "<bug/enhancement>"`
- Report the new issue link back to Telegram.

### Capability 2: Scan & Find Existing Target Issues
- Run `gh issue list --repo <owner/repo> --label "good-first-issue,help wanted" --state open`
- Select an open bug report or feature request.
- Read issue details using `gh issue view <issue_number> --repo <owner/repo>`.

### Capability 3: Fork & Clone Repository
- Fork the target repository: `gh repo fork <owner/repo> --clone=true`
- Checkout a clean working feature branch: `git checkout -b fix-issue-<issue_number>`

### Capability 4: Reproduce & Edit Code
- Locate relevant files and write code fixes.
- Run test suites (`npm test`, `pytest`, etc.).

### Capability 5: Commit, Push & Submit PR
- Add & commit: `git commit -m "fix(#issue): resolve <issue summary>"`
- Push branch: `git push -u origin fix-issue-<issue_number>`
- Submit PR:
  `gh pr create --repo <owner/repo> --title "fix: <summary>" --body "Closes #<issue_number>. <Detailed explanation of fix and tests.>"`
- Report the live Pull Request link back to Telegram!
