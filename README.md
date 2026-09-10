# ☁️ CIEARA

> **An AI agent that turns production crashes into reviewed pull requests — automatically.**

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Prototype-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚩 The Problem

When an application crashes in production, the standard debugging loop looks like this:

`🪵 Read the log` → `🔍 Google the error` → `🕵️ Search the codebase` → `🛠️ Fix the code`

This is slow, repetitive, and pulls engineers away from other work — especially for common, well-understood failure classes like bad connection strings, missing environment variables, or malformed config.

---

## ✨ What CIEARA Does

CIEARA automates that entire loop, end to end:

| Step | Action |
|------|--------|
| 1️⃣ | **Detects** new error entries from Google Cloud Logging |
| 2️⃣ | **Fetches** the actual source code responsible, from GitHub |
| 3️⃣ | **Diagnoses** the root cause using an LLM (Groq) — given both the error *and* the real surrounding code, not just the error message alone |
| 4️⃣ | **Proposes a fix**, shown as a clear diff for human review |
| 5️⃣ | **Waits for explicit approval** before touching the repository |
| 6️⃣ | **Creates a branch and opens a pull request**, with the diagnosis and explanation included |

---

## 🛡️ Why the Approval Step Matters

CIEARA is **deliberately not fully autonomous end-to-end.**

It stops short of merging code on its own — it proposes a PR, the same way a human contributor would, so an engineer always stays in control of what actually reaches production.

> 🔑 This is a deliberate design choice, not a missing feature. Unreviewed, fully autonomous code changes are a real risk in production systems.

---

## 🧰 Tech Stack

- ☁️ **Google Cloud Logging** — error detection
- 🐙 **GitHub API (PyGithub)** — fetching source code, creating branches, opening PRs
- ⚡ **Groq** — diagnosis and fix generation
- 🎨 **Streamlit** — dashboard UI
- 🗄️ **SQLite** — local history of past fixes
- 🐍 **Python** end to end

---

## 🖥️ How It Looks

```
┌─────────────────────────────────────────────┐
│  ☁️ CIEARA                                   │
│                                               │
│  Monitoring: your-gcp-project                │
│  Repository: your-username/your-repo         │
│                                               │
│  [ Check for latest error ]                  │
│  [ Diagnose and generate fix ]               │
│  [ Approve and create Pull Request ]         │
│                                               │
│  📜 History of past fixes                    │
└─────────────────────────────────────────────┘
```

---

## ⚠️ Current Limitations

- 🎯 Monitors a **single** pre-configured GCP project + GitHub repository (no automatic multi-service discovery yet)
- 🧪 Tested against a small set of **deliberately introduced** bug types; not yet validated against a large, real-world codebase
- 🔁 No automated **post-merge verification** yet (confirming the error is actually gone after the fix is deployed)

---

## 🚀 Setup

```bash
# clone the repo
git clone <your-repo-url>
cd agent-auditor

# install dependencies with uv
uv add google-cloud-logging PyGithub groq python-dotenv streamlit

# add your keys to .env
GOOGLE_APPLICATION_CREDENTIALS=gcp-key.json
GCP_PROJECT_ID=your-project-id
GITHUB_TOKEN=your-github-token
GITHUB_REPO=your-username/your-repo
TARGET_FILE=bug.py
GROQ_API_KEY=your-groq-api-key

# run the app
uv run streamlit run app.py
```

---

## 🧪 Test Repository

CIEARA was demonstrated against a small sample app with two deliberately introduced bugs (a database connection failure and a missing environment variable):

[![Test Repo](https://img.shields.io/badge/Test%20Repo-test--log--auditor-blueviolet?logo=github)](https://github.com/hajuanas92-code/test-log-auditor)

Clone it, run `python bug.py db` or `python bug.py api` to trigger an error, and point CIEARA's `.env` (`GITHUB_REPO`, `TARGET_FILE`) at your fork to reproduce the full pipeline yourself.

---

## 💡 Why This Matters

CIEARA isn't just a script — it's a working prototype of a category of tool that real engineering teams already pay for (Sentry, Rootly, incident.io, and the broader "AIOps" space). Most existing tools stop at *alerting*; CIEARA goes a step further and proposes an actual fix, while keeping a human firmly in the loop before anything reaches your codebase.

---

## 🔮 What's Next for CIEARA

- **Continuous monitoring**: right now CIEARA checks for errors on demand; the next step is a background polling loop so it truly watches logs in real time without a manual click.
- **Multi-repo support**: currently CIEARA is configured to watch a single GCP project and GitHub repository; extending this to a mapping of multiple services to their respective repos would make it usable across a real team's infrastructure.
- **Post-merge verification**: after a fix is merged, CIEARA could automatically recheck Cloud Logging to confirm the original error has actually stopped occurring, closing the loop completely.
- **Broader bug coverage**: expanding to more error categories (data validation, timeout handling, malformed input) would strengthen its general-purpose claim.
- **Packaging as an installable SDK**: a small pip-installable library could handle error capture automatically for any Python (and eventually other language) codebase.

---

<p align="center">Built with 🐍 Python, ☁️ GCP, ⚡ Groq, and a lot of debugging.</p>
