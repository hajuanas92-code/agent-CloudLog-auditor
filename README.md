Cloud Log Auditor

An autonomous agent that detects production errors, diagnoses their root cause with AI, and proposes a fix as a pull request — with human approval before anything is written to your codebase.

The Problem

When an application crashes in production, the standard debugging loop looks like this: an engineer notices the error (often after the fact), reads through the raw log, searches for the error message online, manually traces it back to the relevant file and line in the codebase, and finally writes and tests a fix. This is slow, repetitive, and pulls engineers away from other work — especially for common, well-understood failure classes (bad connection strings, missing environment variables, malformed config).

What This Does

Cloud Log Auditor automates that loop end-to-end:

Detects new error entries from Google Cloud Logging
Fetches the actual source code responsible, from GitHub
Diagnoses the root cause using an LLM (Groq), given both the error and the real surrounding code — not just guessing from the error message alone
Proposes a fix, shown as a clear diff for human review
Waits for explicit approval before touching the repository
Creates a branch and opens a pull request, with the diagnosis and explanation included, so the fix goes through the same review process as any other code change
Why the approval step matters

This agent is deliberately not fully autonomous end-to-end. It stops short of merging code on its own — it proposes a PR, the same way a human contributor would, so an engineer stays in control of what actually reaches production. This is a deliberate design choice, not a missing feature: unreviewed, fully autonomous code changes are a real risk in production systems.

Tech Stack
Google Cloud Logging — error detection
GitHub API (PyGithub) — fetching source code, creating branches, opening PRs
Groq (Llama 3.3) — diagnosis and fix generation
Streamlit — dashboard UI
SQLite — local history of past fixes
Python end to end
Current Limitations
Monitors a single pre-configured GCP project + GitHub repository (not automatic multi-service discovery)
Tested against a small set of deliberately introduced bug types; not yet validated against a large, real-world codebase
No automated post-merge verification yet (confirming the error is actually gone after the fix is deployed)
